import sys, pygame
import numpy as np
import math
from robot import Robot, limAng



pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf = font.render(s, True, (0, 0, 0))
    screen.blit(surf, (x, y))

sz = (800, 600)

def main():
    samples = []

    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    robot = Robot(100, 100, 1)

    time = 0
    iFrame=0
    goal = [300, 400]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit(0)
        dt = 1 / fps
        screen.fill((255, 255, 255))

        dx=goal[0] - robot.x
        dy=goal[1] - robot.y
        da=limAng(math.atan2(dy, dx) - robot.alpha)

        robot.goto(goal, dt)
        theta=robot.steerVelocity

        robot.sim(dt)
        robot.draw(screen)

        if iFrame%(fps//4)==0:
            sample = [dx, dy, da, theta]
            samples.append(sample)
            goal=[np.random.randint(0, sz[0]),
                np.random.randint(0, sz[1])]
            if len(samples)==300:
                with open("samples.txt", "w") as f:
                    f.write(str(samples))
                with open("traj.txt", "w") as f:
                    f.write(str(robot.traj))
                pygame.image.save(screen, "simulation.png")
                sys.exit(0)

        pygame.draw.circle(screen, (255, 0, 0), goal, 5, 2)

        drawText(screen, f"Time = {time:.3f}", 5, 5)
        drawText(screen, f"Num Samples = {len(samples)}", 5, 25)

        pygame.display.flip()
        timer.tick(fps)
        time += dt
        iFrame+=1


main()

# template file by S. Diane, RTU MIREA, 2024