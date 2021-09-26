import pygame, time


class PxlEngine:
    def __init__(self, w, h, pixel_w, pixel_h, name='PixelEngineProject'):
        pygame.init()
        self.screen_size = self.screen_w, self.screen_h = w, h
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(name)
        self.p_w, self.p_h = pixel_w, pixel_h
        self.Sprites = pygame.sprite.Group()
        self.t_keys = []
        self.d = 0

    def on_user_update(self, time_delta):
        pass

    def run(self):
        tp1 = time.process_time()
        running = True

        while running:
            tp2 = time.process_time()
            tdelta = tp2 - tp1
            tp1 = tp2

            self.on_user_update(tdelta)
            self.t_keys = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key:
                        self.t_keys.append(pygame.key.name(event.key))
            pygame.display.flip()

        pygame.quit()

    def draw(self, x, y, rgb_tuple):
        pygame.draw.rect(self.screen, rgb_tuple, (x, y, self.p_w, self.p_h))

    def draw_triangle(self, xy1, xy2, xy3, col, w=0):
        pygame.draw.polygon(self.screen, col, [xy1, xy2, xy3], w)

    def draw_line(self, x1, y1, x2, y2, col):
        pygame.draw.line(self.screen, col, (x1, y1), (x2, y2))

    def fill_screen(self, col):
        self.screen.fill(col)

    def is_key_pressed(self, key):
        return pygame.key.get_pressed()[pygame.key.key_code(key)]



if __name__ == '__main__':
    test = PxlEngine(600, 300, 4, 4)
    test.run()
