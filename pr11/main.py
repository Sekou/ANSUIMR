
import sys, pygame
import numpy as np
import math


fps = 20
GRASS_REGROWTH_TIME=60/fps

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

def rnd(x1, x2):
    return x1+(x2-x1)*np.random.random()


sz = (800, 600)


class Cell:
    def __init__(self, x, y, sz):
        self.x, self.y, self.sz =x, y, sz
        self.countdown=0
        self.hasGrass=False
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        pose=[self.x-self.sz/2, self.y-self.sz/2, self.sz,self.sz]
        color=(0,255,0) if self.hasGrass else (255,255,255)
        pygame.draw.rect(screen, color, pose, 0)
        pygame.draw.rect(screen, (0,0,0), pose, 2)
    def sim(self, dt):
        if self.countdown>GRASS_REGROWTH_TIME:
            self.hasGrass=True
        else:
            self.countdown += dt
            self.hasGrass=False

class Agent:
    def __init__(self, x, y, type, sz):
        self.x, self.y, self.type, self.sz = x, y, type, sz
        self.color = (255, 255, 255) if type=="sheep" else (0,0,0)
        self.targetPos=None
        self.targetCell=None
        self.targetAgent=None
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        x,y,sz=self.x, self.y, self.sz
        pose = [x - sz / 2, y - sz / 4, sz, sz / 2]
        pygame.draw.ellipse(screen, self.color, pose, 0)
        pygame.draw.ellipse(screen, (0, 0, 0), pose, 2)
        pygame.draw.circle(screen, self.color, [x + sz / 2, y - sz / 4], sz / 4, 0)
        pygame.draw.circle(screen, (0, 0, 0), [x + sz / 2, y - sz / 4], sz / 4, 2)
        for i in range(4):
            p1 = [x - sz / 2 + i * sz / 3, y]
            p2 = [x - sz / 2 + i * sz / 3, y + sz / 2]
            pygame.draw.line(screen, (0, 0, 0), p1, p2, 2)
    def getNearestGrass(self, cells):
        cc=[c for c in cells if c.hasGrass]
        dd=[dist(self.getPos(), c.getPos()) for c in cc]
        if len(dd)>0:
            return cc[np.argmin(dd)]
        else:
            return None
    def sim(self, dt, cells):
        if self.targetCell is None:
            self.targetCell=self.getNearestGrass(cells)
        if self.targetCell is not None:
            self.targetPos=self.targetCell.getPos()
            v=np.subtract(self.targetPos, self.getPos())
            v=50*v/np.linalg.norm(v)*dt
            self.x+=v[0]
            self.y+=v[1]
            d=dist(self.getPos(), self.targetPos)
            if d < self.sz:
                self.targetCell.hasGrass=False
                self.targetCell.countdown=0
                self.targetCell=None

class Grid:
    def __init__(self, x0, y0, sz, nx, ny):
        self.x0, self.y0, self.sz, self.nx, self.ny = \
        x0, y0, sz, nx, ny
        self.cells=[]
        for iy in range(ny):
            row=[]
            for ix in range(nx):
                c=Cell(x0+(ix+0.5)*sz, y0+(iy+0.5)*sz, sz)
                row.append(c)
            self.cells.append(row)
    def getAllCells(self):
        return [c for row in self.cells for c in row]
    def draw(self, screen):
        for cell in self.getAllCells():
            cell.draw(screen)
    def sim(self, dt):
        for cell in self.getAllCells():
            cell.sim(dt)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()

    # cell = Cell(200, 200, 30)
    grid = Grid(200,200,30,10,10)

    agents=[]
    for i in range(10):
        x=rnd(grid.x0, grid.x0+grid.sz*grid.nx)
        y=rnd(grid.y0, grid.y0+grid.sz*grid.ny)
        a=Agent(x,y,"sheep",30)
        agents.append(a)

    for c in grid.getAllCells():
        c.countdown=rnd(0, GRASS_REGROWTH_TIME)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        dt=1/fps

        grid.sim(dt)

        for a in agents:
            a.sim(dt, grid.getAllCells())

        screen.fill((255, 255, 255))
        grid.draw(screen)

        for a in agents:
            a.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()
#template file by S. Diane, RTU MIREA, 2024