import hungarian_algorithm
import tank2d
import sys, pygame
import numpy as np
import math

pygame.font.init()
def drawText(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    font = pygame.font.SysFont('Comic Sans MS', sz)
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

def limAng(a):
    while a>np.pi: a-=np.pi*2
    while a<=-np.pi: a+=np.pi*2
    return a

def getDistMatrix(groupName, tanks):
    tt=[t for t in tanks if groupName in t.id and t.health>0]
    enemies=[t for t in tanks if not t in tt and t.health>0]
    res=np.zeros((len(tt), len(enemies)))
    for iy,t in enumerate(tt):
        for ix,e in enumerate(enemies):
            res[iy, ix] = int(tank2d.dist(t.getPos(), e.getPos()))
    return res

def planAttack2(groupName, tanks):
    tt=[t for t in tanks if groupName in t.id and t.health>0]
    enemies=[t for t in tanks if not t in tt and t.health>0]
    if len(tt)==0 or len(enemies)==0:
        for tank in tt:
            tank.enemy = None
        return
    mat=getDistMatrix(groupName, tanks)
    assignment=hungarian_algorithm.findAssignments(mat)
    for i, t in enumerate(tt):
        t.enemy=enemies[assignment[i]]

def planAttack(groupName, tanks):
    tt=[t for t in tanks if groupName in t.id and t.health>0]
    enemies=[t for t in tanks if not t in tt and t.health>0]
    for tank in tt:
        tank.enemy=None
        dd=[tank2d.dist(tank.getPos(), enemy.getPos()) for enemy in enemies]
        if len(dd)==0: continue
        i = np.argmin(dd)
        tank.enemy = enemies[i]

def controlTanks(tanks, bullets):
    for tank in tanks:
        if tank.enemy is None: continue
        da1=limAng(math.atan2(tank.enemy.y-tank.y, tank.enemy.x-tank.x) - tank.ang)
        da2=limAng(math.atan2(tank.enemy.y-tank.y, tank.enemy.x-tank.x) - (tank.ang+tank.angGun))
        tank.va=0.5*da1 #скорость поворота корпуса
        tank.vx=50 #скорость линейного движения
        tank.vaGun=2*da2 #скорость поворота турели
        if tank.fireWait>=0.5: #стреляем с задержкой
            bullets.append(tank.fire())
            tank.fireWait=0

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20
    time=0
    totalTime=0
    FINISHED = False

    bullets=[]
    tanks = [
        tank2d.Tank("red-1", 100, 200, 1),
        tank2d.Tank("red-2", 100, 300, 1),
        tank2d.Tank("red-3", 100, 400, 1),
        tank2d.Tank("red-4", 100, 500, 1),

        tank2d.Tank("green-1", 100, 50, 2),
        tank2d.Tank("green-2", 200, 50, 2),
        tank2d.Tank("green-3", 300, 50, 2),
        tank2d.Tank("green-4", 400, 50, 2),

        tank2d.Tank("blue-1", 500, 200, 3),
        tank2d.Tank("blue-2", 500, 300, 3),
        tank2d.Tank("blue-3", 500, 400, 3),
        tank2d.Tank("blue-4", 500, 500, 3),
    ]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    mat=getDistMatrix("red", tanks)
                    print(mat)
                    pygame.image.save(screen, "screenshot.png")

        dt=1/fps
        screen.fill((255, 255, 255))

        names=["red", "green", "blue"]

        for name in names:
            if name=="red":
                planAttack2(name, tanks) #используем венгерский алгоритм
            else:
                planAttack2(name, tanks) #используем жадное назначений

        controlTanks(tanks, bullets)

        for tank in tanks: tank.sim(dt)
        for bullet in bullets: bullet.sim(dt)
        for tank in tanks: tank.draw(screen)
        for tank in tanks:
            if tank.health>0:
                dx=np.array(5*(2-np.random.rand()))
                dy=np.array(5*(2-np.random.rand()))
                if tank.enemy is not None:
                    pygame.draw.line(screen, tank.getColor(),
                                     tank.getPos()+dx, tank.enemy.getPos()+dy, 1)

        for bullet in bullets: bullet.draw(screen)

        for b in bullets:
            for t in tanks:
                d=tank2d.dist(b.getPos(), t.getPos())
                if d<tank.L/2:
                    b.x=-100500
                    t.health=max(0,t.health-25)

        bullets = [b for b in bullets if not (b.x<0 or b.x>sz[0] or b.y<0 or b.y>sz[1])]

        drawText(screen, f"Test = {1}", 5, 5)
        drawText(screen, f"Time = {time:.2f}", 5, 25)
        drawText(screen, f"Total Time = {totalTime:.2f}", 5, 45)

        pygame.display.flip()
        timer.tick(fps)
        time+=dt

        if not FINISHED:
            for name in names:
                if all((name in t.id) for t in tanks if t.health>0):
                    FINISHED=True
                    totalTime=time
                    break




main()