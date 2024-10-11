import sys, pygame
import numpy as np
import math

#TODO: для правильного расчета энергии желательно 
# измерять координаты робота в метрах а не пикселях

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

def rot(v, ang): #функция для поворота на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang):
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

def drawRotRect(screen, color, pc, w, h, ang): #точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [
        [- w/2, - h/2],
        [+ w/2, - h/2],
        [+ w/2, + h/2],
        [- w/2, + h/2],
    ]
    pts = rotArr(pts, ang)
    pts = np.add(pts, pc)
    pygame.draw.polygon(screen, color, pts, 2)

class ControlStrategy:
    def __init__(self):
        self.actions=[]
        self.ind=0
    def getCopy(self):
        res=ControlStrategy()
        res.actions=np.array(self.actions).tolist()
        return res

class Robot:
    def __init__(self, x, y, alpha, m):
        self.m=m
        self.x=x
        self.y=y
        self.alpha=alpha
        self.xLast=x
        self.yLast=y
        self.alphaLast=alpha
        self.L=70
        self.W=40
        self.speed=0
        self.steer=0
        self.traj=[] #точки траектории
        self.lostEnergy=0
        self.color=[0,0,255]
        
    def getPos(self):
        return [self.x, self.y]
    def clear(self):
        self.traj = []
        self.vals1 = []
        self.vals2 = []

    def draw(self, screen):
        p=np.array(self.getPos())
        drawRotRect(screen, (0,0,0), p,
                    self.L, self.W, self.alpha)
        dx=self.L/3
        dy=self.W/3
        dd=[[-dx,-dy], [-dx,dy], [dx,-dy], [dx,dy]]
        dd=rotArr(dd, self.alpha)
        kRot=[0,0,1,1]
        for d, k in zip(dd, kRot):
            drawRotRect(screen, (0, 0, 0), p+d,
                        self.L/5, self.W/5, self.alpha+k*self.steer)
        for i in range(len(self.traj)-1):
            pygame.draw.line(screen, self.color, self.traj[i], self.traj[i+1], 1)
    def sim(self, dt):
        self.addedTrajPt = False
        delta=[self.speed*dt, 0]
        delta=rot(delta, self.alpha)
        self.xLast=self.x
        self.yLast=self.y
        self.alphaLast=self.alpha
        self.x+=delta[0]
        self.y+=delta[1]
        if self.steer!=0:
            R = self.L/self.steer
            da = self.speed*dt/R
            self.alpha+=da

        p=self.getPos()
        if len(self.traj)==0 or dist(p, self.traj[-1])>10:
            self.traj.append(self.getPos())
            self.addedTrajPt=True
        self.lostEnergy+=1000*dt

    def goto(self, pos, dt):
        v=np.subtract(pos, self.getPos())
        aGoal=math.atan2(v[1], v[0])
        da=limAng(aGoal-self.alpha)
        self.steer += 1 * da * dt
        maxSteer=1
        if self.steer > maxSteer: self.steer = maxSteer
        if self.steer < -maxSteer: self.steer = -maxSteer
        self.speed = 50
    def calcEnergy(self, dt):
        v=dist(self.getPos(), [self.xLast, self.yLast])/dt
        eLin=self.m*v**2/2
        j=self.m/12*(self.W**2+self.L**2)
        w=(self.alpha-self.alphaLast)/dt
        eRot=j*w**2/2
        return eLin+eRot+self.lostEnergy

def evalControlStrategy(robot, cs, dt, tMax=15):
    time=0
    while time<tMax:
        tt=[abs(c[0]-time) for c in cs.actions]
        i=np.argmin(tt)
        if time>cs.actions[i][0]:
            cs.ind=i

        control=cs.actions[cs.ind]
        robot.speed=control[1]
        robot.steer=control[2]
        robot.sim(dt)
        time+=dt
def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    QMax=0
    csBest=None

    def rn(a, b):
        return a+(b-a)*np.random.random()

    def createRobot():
        robot=Robot(100, 100, 1, 100)
        cs = ControlStrategy()
        # cs.actions=[
        #     [0, 50, 0.3],#в момент времени 0 подаем линейную скорость 50 и поворот колес 1 радиан
        #     [5, 50, -1],
        #     [10, 0, 0]
        #     ]
        cs.actions=[
        [0, rn(40,70), rn(-1,1)],#в момент времени 0 подаем линейную скорость 50 и поворот колес 1 радиан
        [5, rn(40,70), rn(-1,1)],
        [10, 0, 0]
        ]
        return robot, cs 
    robot, cs=createRobot()

    goal = [500,400]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_1:
                    time=0
                    robot, cs=createRobot()
                
        dt=1/fps
        screen.fill((255, 255, 255))


        timeMax=15
        robot, cs=createRobot()
        evalControlStrategy(robot, cs, dt, timeMax)
        #robot.goto(goal, dt)


        E=robot.calcEnergy(dt)
        d=dist(robot.getPos(), goal)
        Q=1/math.sqrt(d*E)

        if Q>QMax:
            QMax=Q
            csBest=cs.getCopy()
        
        #текущая стратегия
        robot.draw(screen)

        robot, cs=createRobot()
        robot.color=[0,255,0]
        evalControlStrategy(robot, csBest, dt, timeMax)

        #лучшая на данный момент стратегия
        robot.draw(screen)

        
        pygame.draw.circle(screen, (255,0,0), goal, 5, 2)
        drawText(screen, f"Time = {timeMax:.3f}", 5, 5)
        drawText(screen, f"Energy = {E:.3f}", 5, 25)
        drawText(screen, f"Control Ind = {cs.ind}", 5, 45)
        drawText(screen, f"Goal Dist = {d:.1f}", 5, 65)
        drawText(screen, f"Q = {Q:.5f}", 5, 85)

       
        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024