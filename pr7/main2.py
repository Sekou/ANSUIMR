import sys, pygame
import numpy as np
import math
from robot import Robot, limAng
from train_net2 import createModel

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf = font.render(s, True, (0, 0, 0))
    screen.blit(surf, (x, y))

sz = (800, 600)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    robot = Robot(100, 100, 1)

    time = 0
    iFrame=0
    goal = [300, 400]

    net=createModel()
    net.load_weights("net.weights.h5")

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit(0)
        dt = 1 / fps
        screen.fill((255, 255, 255))

        input=[robot.x/100, robot.y/100, goal[0]/100, goal[1]/100, robot.alpha]
        output=net.predict(np.array([input]))
        robot.steerVelocity=output[0][0]
        robot.speed=50

        # robot.goto(goal, dt)
        # theta=robot.steerVelocity

        robot.sim(dt)
        robot.draw(screen)

        if iFrame%(fps//4)==0:
            goal=[np.random.randint(0, sz[0]),
                np.random.randint(0, sz[1])]

        pygame.draw.circle(screen, (255, 0, 0), goal, 5, 2)

        drawText(screen, f"Time = {time:.3f}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)
        time += dt
        iFrame+=1

main()

# template file by S. Diane, RTU MIREA, 2024