import sys, pygame
import numpy as np
import math

pygame.font.init()
def drawText(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    font = pygame.font.SysFont('Comic Sans MS', sz)
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang): #ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2): #расстояние между точками
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

sz = (800, 600)

pts=[
    [210,200],
    [310,280],
    [650,310],
    [350,230],
    [260,270],
    [420,330],
    [620,230],
    [480,290],
    [210,310],
    [460,200]
]

class Edge:
    def __init__(self, n1, n2, w):
        self.n1=n1
        self.n2=n2
        self.w=w
    def draw(self, screen):
        pygame.draw.line(screen, (0,0,255), self.n1.getPos(), self.n2.getPos())

class Node:
    def __init__(self, x, y):
        self.x, self.y=x, y
        self.nextEdges=[]
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.getPos(), 4, 0)
        for e in self.nextEdges:
            e.draw(screen)

class Graph:
    def __init__(self, pts):
        self.nodes=[Node(*p) for p in pts]
    def draw(self, screen):
        for n in self.nodes:
            n.draw(screen)
    def connect(self):
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1==n2: continue
                w=dist(n1.getPos(), n2.getPos())
                n1.nextEdges.append(Edge(n1, n2, w))

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    graph=Graph(pts)
    graph.connect()

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        dt=1/fps

        screen.fill((255, 255, 255))

        graph.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024