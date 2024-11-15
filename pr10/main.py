import sys, pygame
import numpy as np
import math

pygame.font.init()
def drawText(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    font = pygame.font.SysFont('Comic Sans MS', sz)
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

#отрисовка центрованного квадрата
def drawSquare(screen, ptCenter, size):
    pygame.draw.rect(screen, (0, 0, 0),
                     [ptCenter[0] - size/2, ptCenter[1] - size/2, size, size], 2)

class Grid:
    def __init__(self, nx, ny):
        self.x0=100
        self.y0=100
        self.nx=nx
        self.ny=ny
        self.sz=45
    def draw(self, screen):
        nn=self.getNodes()
        for n in nn:
            drawSquare(screen,
                       [n[0]+0.5*self.sz, n[1]+0.5*self.sz], self.sz)
    def getNodes(self):
        nodes=[]
        for iy in range(self.ny):
            for ix in range(self.nx):
                x, y=self.x0+(ix+0.5)*self.sz, self.y0+(iy+0.5)*self.sz
                nodes.append([x, y])
        return nodes


class Edge:
    def __init__(self, n1, n2, w):
        self.n1 = n1
        self.n2 = n2
        self.w = w

class Node:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.edges=[]

class Graph:
    def __init__(self, nodePoints, nx, ny):
        self.nx=nx
        self.ny=ny
        self.nodes=[]
        i=0
        for iy in range(self.ny):
            row=[]
            for ix in range(self.nx):
                p=nodePoints[i]
                node=Node(*p)
                row.append(node)
                i += 1
            self.nodes.append(row)
    def connect(self):
        neighborhood=[[0, -1], [1, 0], [0, 1], [-1, 0]]
        for iy in range(self.ny):
            for ix in range(self.nx):
                n1=self.nodes[iy][ix]
                for i, j in neighborhood:
                    if 0<=iy+j<self.ny and 0<=ix+i<self.nx:
                        n2 = self.nodes[iy+j][ix+i]
                        edge=Edge(n1, n2, 1)
                        n1.edges.append(edge)
    def draw(self, screen):
        for n in self.nodes:
            pygame.draw.circle()

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    grid=Grid(10, 7)

    graph = Graph(grid.getNodes(), 10, 7)
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

        grid.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()