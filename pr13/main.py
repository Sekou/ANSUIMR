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

def probSel(probs):
    m, s=sum(probs), 0
    if m==0: return np.random.randint(len(probs))
    probs=[p/m for p in probs]
    r=np.random.rand()
    for i in range(len(probs)):
        s+=probs[i]
        if s>=r: return i
    return -1

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
        self.pheromone=0
    def draw(self, screen):
        k=1-max(0.1,self.pheromone/100)
        R,G,B=int(255*k),int(255*k),255
        pygame.draw.line(screen, (R,G,B), self.n1.getPos(), self.n2.getPos())
    def incrementPheromone(self, val):
        self.pheromone=min(100, self.pheromone+val)
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

class Ant:
    def __init__(self, node):
        self.currentNode=node
        self.visitedNodes = set([self.currentNode])
        self.visitedEdges = set()
    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), self.currentNode.getPos(), 5, 2)
    def isLost(self):
        return all(e.n2 in self.visitedNodes for e in self.currentNode.nextEdges)
    def isFinished(self, graph):
        return len(self.visitedNodes)==len(graph.nodes)
    def getQ(self):
        return sum(e.pheromone for n in self.visitedNodes for e in n.nextEdges)
    def getQ2(self):
        return sum(e.w for n in self.visitedNodes for e in n.nextEdges)
    def move(self):
        if np.random.random()<0.3:
            ind=np.random.randint(len(self.currentNode.nextEdges))
        else:
            phph=[e.pheromone for e in self.currentNode.nextEdges]
            ind=probSel(phph)
        next=self.currentNode.nextEdges[ind].n2
        if not next in self.visitedNodes:
            e=self.currentNode.nextEdges[ind]
            l=e.w
            e.incrementPheromone(1000/l)
            self.currentNode=next
            self.visitedNodes.add(next)
            self.visitedEdges.add(e)
            return True
        return False


#TODO:
# +оставлять феромон обр.пропорц длине перехода,
# +выбирать переходы с макс. феромоном,
# +не ходить повторно в те же вершины
# +завершать движение при посещении всех вершин

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 50

    graph=Graph(pts)
    graph.connect()

    ant=Ant(graph.nodes[0])

    ants=[]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    ant.move()

        dt=1/fps

        screen.fill((255, 255, 255))

        graph.draw(screen)
        ant.draw(screen)
        if not ant.move():
            if ant.isLost() or ant.isFinished(graph):
                ants.append([ant.getQ(), ant])
                for e in ant.visitedEdges:
                    e.pheromone*=0.95
                ind=np.random.randint(len(graph.nodes))
                ant=Ant(graph.nodes[ind])

        for n in graph.nodes:
            for e in n.nextEdges:
                e.pheromone *= 0.999

        drawText(screen, f"Test = {1}", 5, 5)

        if len(ants)>0:
            ants=sorted(ants, key=lambda a: a[0], reverse=True)
            a=ants[0][1]
            for e in a.visitedEdges:
                p1, p2=e.n1.getPos(),e.n2.getPos()
                pygame.draw.line(screen, (0,255,0), p1, p2, 3)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024