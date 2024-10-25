import sys, pygame
import numpy as np
import math

def dist(p1, p2): #расчет расстояния
    return np.linalg.norm(np.subtract(p1, p2))

def rot(v, ang): #функция для поворота на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

class Bullet:
    def __init__(self, x, y, ang):
        self.x = x
        self.y = y
        self.ang = ang
        self.vx = 200
        self.L = 10
        self.exploded = False
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p0 = self.getPos()
        p1 = [-self.L/2, 0]
        p1=rot(p1, self.ang)
        p2 = [+self.L/2, 0]
        p2=rot(p2, self.ang)
        pygame.draw.line(screen, (0, 0, 0), np.add(p0, p1), np.add(p0, p2), 3)
    def sim(self, dt):
        vec=[self.vx, 0]
        vec=rot(vec, self.ang)
        self.x+=vec[0]*dt
        self.y+=vec[1]*dt

class Tank:
    def __init__(self, id, x, y, ang):
        self.id=id
        self.x=x
        self.y=y
        self.ang=ang
        self.angGun=0
        self.L=45
        self.W=25
        self.vx=0
        self.vy=0
        self.va=0
        self.vaGun=0
        self.health=100
        self.fireWait=0
        self.enemy=0
    def fire(self):
        r = self.W / 2.3
        LGun = self.L / 2
        p2 = rot([r + LGun, 0], self.ang + self.angGun)
        p2=np.add(self.getPos(), p2)
        b=Bullet(*p2, self.ang + self.angGun)
        return b
    def getPos(self):
        return [self.x, self.y]
    def getColor(self):
        color = (0, 0, 0)
        if "red" in self.id: color = (255, 0, 0)
        if "green" in self.id: color = (0, 255, 0)
        if "blue" in self.id: color = (0, 0, 255)
        return color
    def draw(self, screen):
        pts=[[self.L/2, self.W/2], [self.L/2, -self.W/2], [-self.L/2, -self.W/2], [-self.L/2, self.W/2]]
        pts=rotArr(pts, self.ang)
        pts=np.add(pts, self.getPos())
        color=self.getColor()
        pygame.draw.polygon(screen, color, pts, 2)
        if self.health==0:
            pygame.draw.polygon(screen, (0,0,0), pts, 0)
        r=self.W/2.3
        pygame.draw.circle(screen, color, self.getPos(), r, 2)
        LGun=self.L/2
        p0=self.getPos()
        p1=rot([r, 0], self.ang+self.angGun)
        p2=rot([r+LGun, 0], self.ang+self.angGun)
        pygame.draw.line(screen, color, np.add(p0, p1), np.add(p0, p2), 3)
        drawText(screen, f"{self.id} ({self.health})", self.x, self.y - self.L/2 - 12)
    def sim(self, dt):
        if self.health<=0: return
        vec=[self.vx, self.vy]
        vec=rot(vec, self.ang)
        self.x+=vec[0]*dt
        self.y+=vec[1]*dt
        self.ang+=self.va*dt
        self.angGun+=self.vaGun*dt
        self.fireWait+=dt
