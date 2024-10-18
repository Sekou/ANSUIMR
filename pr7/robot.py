import pygame
import numpy as np
import math

def rot(v, ang):  # функция для поворота на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang):
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang):  # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

def drawRotRect(screen, color, pc, w, h, ang):  # точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [
        [- w / 2, - h / 2],
        [+ w / 2, - h / 2],
        [+ w / 2, + h / 2],
        [- w / 2, + h / 2],
    ]
    pts = rotArr(pts, ang)
    pts = np.add(pts, pc)
    pygame.draw.polygon(screen, color, pts, 2)

class Robot:
    def __init__(self, x, y, alpha):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.L = 70
        self.W = 40
        self.speed = 0
        self.steer = 0
        self.steerVelocity = 0
        self.traj = []  # точки траектории

    def getPos(self):
        return [self.x, self.y]

    def clear(self):
        self.traj = []
        self.vals1 = []
        self.vals2 = []

    def draw(self, screen):
        p = np.array(self.getPos())
        drawRotRect(screen, (0, 0, 0), p,
                    self.L, self.W, self.alpha)
        dx = self.L / 3
        dy = self.W / 3
        dd = [[-dx, -dy], [-dx, dy], [dx, -dy], [dx, dy]]
        dd = rotArr(dd, self.alpha)
        kRot = [0, 0, 1, 1]
        for d, k in zip(dd, kRot):
            drawRotRect(screen, (0, 0, 0), p + d,
                        self.L / 5, self.W / 5, self.alpha + k * self.steer)
        for i in range(len(self.traj) - 1):
            pygame.draw.line(screen, (0, 0, 255), self.traj[i], self.traj[i + 1], 1)

    def sim(self, dt):
        self.addedTrajPt = False
        delta = [self.speed * dt, 0]
        delta = rot(delta, self.alpha)
        self.x += delta[0]
        self.y += delta[1]

        self.steer += self.steerVelocity * dt
        maxSteer = 1
        if self.steer > maxSteer: self.steer = maxSteer
        if self.steer < -maxSteer: self.steer = -maxSteer

        if self.steer != 0:
            R = self.L / self.steer
            da = self.speed * dt / R
            self.alpha = limAng(self.alpha+da)

        p = self.getPos()
        if len(self.traj) == 0 or dist(p, self.traj[-1]) > 10:
            self.traj.append(self.getPos())
            self.addedTrajPt = True

    def goto(self, pos, dt):
        v = np.subtract(pos, self.getPos())
        aGoal = math.atan2(v[1], v[0])
        self.steerVelocity = 2 * limAng(aGoal - self.alpha)
        self.speed = 50