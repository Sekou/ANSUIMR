
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


class Terrain:
    def __init__(self, y0, x0, x1, n):
        self.y0,self.heights=y0,[]
        self.x0, self.x1, self.n=x0, x1, n
        for i in range(self.n):
            self.heights.append(200*np.random.random())
    def draw(self, screen):
        dx=(self.x1-self.x0)/self.n
        yPrev=self.y0
        for i in range(self.n):
            y=self.y0-self.heights[i]
            x1=self.x0+i*dx
            x2=x1+dx
            pygame.draw.line(screen, (0,0,0), [x1, yPrev], [x1, y], 2)
            pygame.draw.line(screen, (0,0,0), [x1, y], [x2, y], 2)
            yPrev=y
        for i in range(3*self.n//7, 4*self.n//7):
            self.heights[i]=150

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    terrain=Terrain(500, 0, 800, 50)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")

        dt=1/fps

        screen.fill((255, 255, 255))
        terrain.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024