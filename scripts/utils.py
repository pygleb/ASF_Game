import os

import pygame

images_path = 'assets/images/'
tiles_path = 'assets/tiles/'


def load_image(path):
    try:
        img = pygame.image.load(images_path + path).convert_alpha()
    except:
        print(f'Не удалось загрузить изображение {images_path + path}')
        return None

    # Автоматическое удаление черного фона с картинок
    # img.set_colorkey((0, 0, 0))

    return img


def load_tileset(type):
    variants = []
    for _ in os.listdir(tiles_path + type):
        # проверяем, есть ли следующая картинка в папке
        # если нет, выходим из цикла
        # если есть, добавляем картинку в массив
        path = tiles_path + type + '/' + _
        img = pygame.image.load(path).convert_alpha()
        if img is None:
            break
        variants.append(img)
    return variants
