import math

import numpy as np
import pygame
import bee2d
import flower

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

pygame.font.init()
font=pygame.font.SysFont("Comic Sans MS", 14)
def drawText(screen, str, x, y):
    screen.blit(font.render(str, False, (0,0,0)), (x,y))

class Flower:
    def __init__(self, x, y):
        self.x, self.y=x, y
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        flower.draw_flower(screen, self.x, self.y, (200,180,50), (230, 230, 0))

class Nest:
    def __init__(self, x, y):
        self.x, self.y=x, y
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), self.getPos(), 10, 3)
    def spawnBee(self):
        # rx, ry=np.random.normal(0,5, size=(1, 2))
        rx, ry=np.random.multivariate_normal([0,0], [[25, 0], [0, 25]], 1).T
        return Bee(self.x+rx[0], self.y+ry[0])
    def chooseTarget(self):
        ra=2*math.pi*np.random.random()
        rl=np.random.randint(100,200)
        return [self.x+rl*math.cos(ra), self.y+rl*math.sin(ra)]

class Bee:
    def __init__(self, x, y):
        self.x, self.y, self.a=x, y, 0
        self.v = 50 #скорость продольного движения
        self.wingState=0
        self.target=None
        self.nest=None
        self.metric = 0
        self.nearestFlowers = []
        self.state = 0

    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        bee2d.draw_bee(screen, self.x, self.y, -self.a, self.wingState)
        self.wingState=1-self.wingState
        if self.target is not None:
            pygame.draw.circle(screen, (0,0,0), self.target, 3, 2)
        if self.nest is not None and self.target is not None:
            pygame.draw.line(screen, (0,0,0), self.target, self.nest.getPos(), 2)
        for f in self.nearestFlowers:
            pygame.draw.line(screen, (255,150,150), f.getPos(), self.getPos(), 1)
        drawText(screen, f"{self.metric:.2f}", self.x+20, self.y)

    def sim(self, dt): #исполнительный уровень управления
        s, c = math.sin(self.a), math.cos(self.a)
        self.x+=self.v*c*dt
        self.y+=self.v*s*dt
    def control(self, goal):#тактический уровень управления
        da1=math.atan2(goal[1]-self.y, goal[0]-self.x)
        da2=da1-self.a
        #нормализация угла
        while da2>math.pi: da2-=2*math.pi
        while da2<=-math.pi: da2+=2*math.pi
        #задание угла и скорости
        self.a+=2*da2*dt
        self.v=30
    def behave(self, flowers):# стратегический уровень управления
        if self.state==0 and self.target is not None: #разведка
            self.findNearestFlowers(flowers)
            self.control(self.target)
            if dist(self.getPos(), self.target)<25: self.state=1
        elif self.state==1: #перемещение к гнезду
            self.control(self.nest.getPos())
            if dist(self.getPos(), self.nest.getPos()) < 25: self.state = 2
        else:
            self.v=0

    def findNearestFlowers(self, flowers):
        qq=[100/dist(f.getPos(), self.getPos()) for f in flowers]
        pairs=zip(qq, flowers)
        pairs=sorted(pairs, reverse=True)
        pairs=pairs[:3]
        self.metric=np.sum([pair[0] for pair in pairs])
        self.nearestFlowers=[pair[1] for pair in pairs]

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Отрисовка пчелы")
    clock = pygame.time.Clock()

    running = True

    bees=[]
    nest=Nest(400,300)

    flowers=[]

    def launchBees(bees, nest):
        for b in bees:
            b.nest=nest
            b.target=nest.chooseTarget()
            b.state=0 #разведка
    def gatherBees(bees, nest):
        for b in bees:
            b.nest = nest
            b.target = None
            b.state = 1  # движение к гнезду


    # создание цветков
    for i in range(20):
        rx = np.random.randint(50, 750)
        ry = np.random.randint(50, 550)
        flowers.append(Flower(rx, ry))

    #создание пчел
    for i in range(3):
        b=nest.spawnBee()
        b.nest=nest
        bees.append(b)

    launchBees(bees, nest)

    fps=20
    dt=1/fps

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Очистка экрана
        nest.draw(screen)
        for b in bees: b.draw(screen)
        for f in flowers: f.draw(screen)

        for b in bees: b.behave(flowers) #стратегический + тактический уровень
        for b in bees: b.sim(dt) #исполнительный уровень


        if all(b.state==2 for b in bees):
            if all(b.target is not None for b in bees): #после разведки
                qq=[b.metric for b in bees]
                i = np.argmax(qq)
                winner = bees[i]
                nest.x, nest.y=winner.target
                gatherBees(bees, nest)
            else: #после движения к гнезду
                launchBees(bees, nest)






        pygame.display.flip()  # Обновление экрана
        clock.tick(fps)  # Ограничение FPS

    pygame.quit()