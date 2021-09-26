from math import sin, cos, pi, atan2
import PixelEngine
import pygame


class Pseudo3D_FPS(PixelEngine.PxlEngine):
    def __init__(self, w, h, p_w, p_h):
        super().__init__(w, h, p_w, p_h)
        self.fov = pi / 4
        self.playerA = 0
        self.playerX, self.playerY = 8.0, 5.0
        self.depth = 16.0
        self.speed = 2
        self.sens = 1
        self.wall = pygame.image.load('sprites/BrickWall.png')

    def on_user_update(self, time_delta):
        if self.is_key_pressed('w'):
            self.playerY += cos(self.playerA) * self.speed * time_delta
            self.playerX += sin(self.playerA) * self.speed * time_delta
            if map[int(self.playerY) * map_w + int(self.playerX)] == '#':
                self.playerY -= cos(self.playerA) * self.speed * time_delta
                self.playerX -= sin(self.playerA) * self.speed * time_delta
        if self.is_key_pressed('s'):
            self.playerX -= sin(self.playerA) * self.speed * time_delta
            self.playerY -= cos(self.playerA) * self.speed * time_delta
            if map[int(self.playerY) * map_w + int(self.playerX)] == '#':
                self.playerX += sin(self.playerA) * self.speed * time_delta
                self.playerY += cos(self.playerA) * self.speed * time_delta
        if self.is_key_pressed('d'):
            self.playerX += cos(self.playerA) * self.speed * time_delta
            self.playerY -= sin(self.playerA) * self.speed * time_delta
            if map[int(self.playerY) * map_w + int(self.playerX)] == '#':
                self.playerX -= cos(self.playerA) * self.speed * time_delta
                self.playerY += sin(self.playerA) * self.speed * time_delta
        if self.is_key_pressed('a'):
            self.playerX -= cos(self.playerA) * self.speed * time_delta
            self.playerY += sin(self.playerA) * self.speed * time_delta
            if map[int(self.playerY) * map_w + int(self.playerX)] == '#':
                self.playerX += cos(self.playerA) * self.speed * time_delta
                self.playerY -= sin(self.playerA) * self.speed * time_delta
        if self.is_key_pressed('left'):
            self.playerA -= self.sens * time_delta
        if self.is_key_pressed('right'):
            self.playerA += self.sens * time_delta

        for x in range(0, self.screen_w, 4):

            rayA = (self.playerA - self.fov / 2) + (x / self.screen_w) * self.fov
            d_to_wall = 0
            wall_hit = False
            step = 0.1
            eyeX = sin(rayA)
            eyeY = cos(rayA)
            SampleX = 0.0

            while not wall_hit and d_to_wall < self.depth:
                d_to_wall += step

                testX = int(self.playerX + eyeX * d_to_wall)
                testY = int(self.playerY + eyeY * d_to_wall)

                if testX < 0 or testY < 0 or testX >= map_w or testY >= map_h:
                    wall_hit = True
                elif map[testY * map_w + testX] == '#':
                    wall_hit = True

                    blockMidX = testX + 0.5
                    blockMidY = testY + 0.5

                    tpX = self.playerX + eyeX * d_to_wall
                    tpY = self.playerY + eyeY * d_to_wall

                    testAngle = atan2((tpY - blockMidY), (tpX - blockMidX))

                    if -pi * 0.25 <= testAngle < pi * 0.25:
                        SampleX = tpY - testY
                    if pi * 0.25 <= testAngle < pi * 0.75:
                        SampleX = tpX - testX
                    if -pi * 0.25 > testAngle >= -pi * 0.75:
                        SampleX = tpX - testX
                    if testAngle >= pi * 0.75 or testAngle < -pi * 0.75:
                        SampleX = tpY - testY

            ceiling = self.screen_h / 2 - self.screen_h / d_to_wall
            floor = self.screen_h - ceiling

            for y in range(self.screen_h):
                if y < ceiling:
                    engine.draw(x, y, (0, 0, 0))
                elif floor <= y:
                    b = 1.0 - ((y - self.screen_h / 2) / (self.screen_h / 2))
                    shade = (0, 255 - 255 * b, 0)
                    engine.draw(x, y, shade)
                else:
                    shade = (255 - 255 * (max(0, min(d_to_wall, self.depth)) / self.depth), 0, 0)
                    engine.draw(x, y, shade)
            # wallS = pygame.transform.scale(self.wall, (self.wall.get_rect().w, int(self.screen_h - 2 * ceiling)))
            # wallC = pygame.transform.chop(wallS, (int(SampleX * self.wall.get_rect().w), 0, 4, wallS.get_rect().h))
            # self.screen.blit(wallC, (x, ceiling))


def separate(string, w):
    output = []
    for i in range(w, len(string), w):
        output.append(string[i - w:i])
    output.append(string[i:])
    return output


if __name__ == '__main__':
    map = '################################' \
          '#..............#...............#' \
          '#..............#...............#' \
          '#..........#####...........#####' \
          '#..............#...............#' \
          '#..............#...............#' \
          '#..............#...............#' \
          '#..............................#' \
          '#....######....................#' \
          '#..................#####.......#' \
          '#......................#.......#' \
          '######.................#.......#' \
          '#..........#...................#' \
          '#..........#...................#' \
          '#..........#...................#' \
          '#..........#####################'
    map_size = map_w, map_h = 32, 16
    engine = Pseudo3D_FPS(600, 300, 4, 4)
    engine.run()
