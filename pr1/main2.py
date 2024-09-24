import itertools
import sys, pygame
import numpy as np
import math

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

class Obstacle:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.R=30
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), self.getPos(), self.R, 2)

class Robot:
    def __init__(self, x, y, alpha):
        self.x=x
        self.y=y
        self.alpha=alpha
        self.L=70
        self.W=40
        self.speed=0
        self.steer=0
        self.traj=[]
        self.A=3 #стремление к цели
        self.B=2 #боязнь столкновений
    def getPos(self):
        return [self.x, self.y]

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
            pygame.draw.line(screen, (0,0,255), self.traj[i], self.traj[i+1], 1)
    def sim(self, dt):
        delta=[self.speed*dt, 0]
        delta=rot(delta, self.alpha)
        self.x+=delta[0]
        self.y+=delta[1]
        if self.steer!=0:
            R = self.L/self.steer
            da = self.speed*dt/R
            self.alpha+=da

        p=self.getPos()
        if len(self.traj)==0 or dist(p, self.traj[-1])>10:
            self.traj.append(self.getPos())

    def goto(self, pos, obsts, dt):
        #1
        v=np.subtract(pos, self.getPos())
        aGoal=math.atan2(v[1], v[0])
        da=limAng(aGoal-self.alpha)
        #2
        dd=[dist(self.getPos(), o.getPos()) for o in obsts]
        i = np.argmin(dd)
        v2=np.subtract(obsts[i].getPos(), self.getPos())
        aObst=math.atan2(v2[1], v2[0])
        da2 = limAng(aObst - self.alpha)
        #3
        self.steer += (self.A*da-self.B*da2) * dt
        if self.steer > 1: self.steer = 1
        if self.steer < -1: self.steer = -1
        self.speed = 50

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    r=Robot(100,100,1)
    with open('log.txt', 'w') as f: f.write("")

    AA=[5, 7, 10] #варианты коэфф-та движения к цели
    BB=[5, 7, 10] #варианты коэфф-та отталкивания от препятствий
    variants=list(itertools.product(AA, BB))

    indVariant=0

    obsts=[Obstacle(200,200), Obstacle(400,300), Obstacle(270,350), Obstacle(250,450)]

    goal=[500,500]

    time=0

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        dt=1/fps

        screen.fill((255, 255, 255))

        r.A, r.B = 10,5 #variants[indVariant]
        r.goto(goal, obsts, dt)
        r.sim(dt)
        r.draw(screen)

        for o in obsts:
            o.draw(screen)

        pygame.draw.circle(screen, (255,0,0), goal, 5, 2)

        drawText(screen, f"Time = {time:.3f}", 5, 5)
        drawText(screen, f"Variant = {indVariant+1}/{len(variants)}", 5, 25)
        drawText(screen, f"A {r.A}; B {r.B}", 5, 45)

        if dist(r.getPos(), goal)<50 or time>20:

            L=0
            for i in range(len(r.traj)-1):
                L+=dist(r.traj[i], r.traj[i+1])
            N=0
            for i in range(len(r.traj)):
                d=min(dist(r.traj[i], o.getPos()) for o in obsts)
                if d<50: N+=1
            M=len(obsts)
            with open('log.txt', 'a') as f:
                f.write(f"{indVariant}; {r.A}; {r.B}; {time:.3f}; {M}; {L}; {N}; {str(r.traj)}\n")
                print(f"Tested indVariant: {indVariant}")
            indVariant+=1
            r.traj=[]
            r = Robot(100, 100, 1)
            time=-dt #zero
            if indVariant>=len(variants):
                break

        pygame.display.flip()
        timer.tick(fps)
        time+=dt

main()

#template file by S. Diane, RTU MIREA, 2024