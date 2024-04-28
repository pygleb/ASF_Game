import pygame
import random

from scripts.entities.static_object import StaticObject


# описывает поведение каждого объекта, который НЕ может быть подвергнут
# гравитационному воздействию и может обновляться
class UpdatableObject(StaticObject):
    def update(self):
        pass


class Enemy(UpdatableObject):
    def __init__(self, game, x, y):
        # создание изображения для спрайта
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))

        # инициализируем класс-предок
        super().__init__(game=game, entity_type='Enemy', image_asset=self.image, pos=(x, y))

        # начальная позиция по Х, нужна для патрулирования
        self.x_start = x

        # выбор направления начального движения
        self.direction = random.choice([-1, 1])

        # компоненты скорости по оси Х и Y
        self.x_velocity = 1
        self.y_velocity = 0

    def update(self):
        # если расстояние от начальной точки превысило 50,
        # то меняем направление
        if abs(self.x_start - self.rect.x) > 50:
            self.direction *= -1

        # движение спрайта по оси Х
        self.rect.x += self.x_velocity * self.direction
        self.pos[0] += self.x_velocity * self.direction