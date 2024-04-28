import pygame

# Физические константы
max_fall_velocity = 1000


# описывает поведение каждого объекта, который НЕ может быть подвергнут
# гравитационному воздействию и не обновляется
class StaticObject:
    def __init__(self, game, entity_type, image_asset, pos):
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.image_asset = image_asset

        self.size = (image_asset.get_size())

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.velocity = [0, 0]

        # словарь с проверкой коллизии по 4 стороны Rect
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        #заводим переменную-флаг, отображающую наличие поверхности для отталкивания
        self.on_ground=True

    # получить Rect текущего физического объекта
    def getrect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    # функция, отрисовывающая физический объект
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.image_asset, (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Platform(StaticObject):
    def __init__(self, game, x, y, width, height):
        # создание изображения для спрайта
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))

        super().__init__(game, 'platform', self.image, (x, y))

class Collectible(StaticObject):
    def __init__(self, game, x, y):
        # создание изображения для спрайта
        GOLD = (255, 215, 0)
        self.image = pygame.Surface((16, 16))
        self.image.fill(GOLD)

        super().__init__(game, 'collectible', self.image, (x, y))
