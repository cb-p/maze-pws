import pygame


class Button:
    def __init__(self, text, font, x, y, width, height):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hover = False
        self.down = False
        self.pressed = False
        self.disabled = False

    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.hover = True
        else:
            self.hover = False

        if self.hover and not self.disabled:
            if pygame.mouse.get_pressed()[0]:
                if not self.down:
                    self.down = True
                    self.pressed = True
                else:
                    self.pressed = False
            else:
                self.down = False
                self.pressed = False
        else:
            self.down = False
            self.pressed = False

        return self.pressed

    def set_text(self, text):
        self.text = text

    def set_disabled(self, disabled):
        self.disabled = disabled

    def draw(self, surface):
        color = (255, 255, 255)
        if self.hover or self.disabled:
            color = (228, 228, 228)
        if self.down and not self.disabled:
            color = (200, 200, 200)

        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height), 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_x = self.x + self.width / 2 - text_surface.get_width() / 2
        text_y = self.y + self.height / 2 - text_surface.get_height() / 2 + 2
        surface.blit(text_surface, (text_x, text_y))
