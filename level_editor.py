# Управление
# Передвижение:                             стрелочки на клавиатуре
#
# Изменить скорость полёта:                 + или - или num+ или num- (Осторожно, может уйти в минус, много не нажимайте!)
#
# Изменить тайл
# (папки testblock, floor):                 колесо мыши
#
# Изменить версию тайла
# (файлы 0.png, 1.png, 2.png и т.д.):       shift+колесо мыши
#
# Сохранить:                                O (английская буква O)
#
# Изменить декор/блоки:                     g
#
# Поставить блок:                           ЛКМ
# Убрать блок:                              ПКМ
#
# Карта пока что только одна, но при желании вы можете сохранять их отдельно и сделать несколько.
# Свои картинки тайлов (размер 64х64) или декора (любой размер) добавлять в assets/tiles/[название тайла]
#
# Для запуска редактора просто запустите этот файл. Игра запустит сохраненный на букву О файл "map.json".
#
# Миша, сделай двойной прыжок!


import pygame

# подключение библиотек
from scripts.tilemap import Tilemap, Tile
from scripts.utils import *

# константы-параметры окна
WIDTH = 800
HEIGHT = 600
D_WIDTH = 800
D_HEIGHT = 600
RENDER_SCALE = 1.0
DEFAULT_CAM_SPEED = 5
# константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
# путь до заднего фона редактора
BACKGROUND_PATH = 'background.png'


class LevelEditor:
    def __init__(self):
        # инициализация Pygame
        self.collision_objects = []
        pygame.init()

        # инициализация движения
        self.movement = [False, False, False, False]
        # инициализация нажатия кнопок мыши
        self.left_click = False
        self.right_click = False
        # инициализация вспомогательных кнопок
        self.shift = False

        # инициализация дополнительных переменных
        self.ongrid = False
        self.cam_speed = DEFAULT_CAM_SPEED

        # создаем экран + дисплей, счетчик частоты кадров и очков
        pygame.display.set_caption('ASF_LevelEditor')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((D_WIDTH, D_HEIGHT))
        self.clock = pygame.time.Clock()

        # подгружаем текстуры
        self.assets = {
            # тайлы
            'testblock': load_tileset('testblock'),
            'background-tiles': load_tileset('background'),
            'interior_walls_1': load_tileset('interior_walls_1')
        }

        # создаем карту из тайлмапа
        self.tm = Tilemap(self)

        try:
            self.tm.load('map.json')
        except FileNotFoundError:
            pass

        # используемый набор тайлов, инициализация необходимых переменных
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # позиция камеры
        self.camera_position = [0, 0]

        # загружаем фон
        self.background = pygame.transform.scale(load_image(BACKGROUND_PATH), (WIDTH, HEIGHT))

        # игровой цикл
        self.running = True

    # основной игровой цикл
    def run(self):
        while self.running:

            # проверка ввода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # если нажата левая кнопка мыши
                    if event.button == 1:
                        self.left_click = True
                        if not self.ongrid:
                            self.tm.offgrid_tiles.append(Tile(type=self.tile_list[self.tile_group],
                                                              variant=self.tile_variant,
                                                              position=(mousepos[0] + self.camera_position[0],
                                                                        mousepos[1] + self.camera_position[1])
                                                              ))
                    # если нажата правая кнопка мыши
                    if event.button == 3:
                        self.right_click = True
                    if self.shift:
                        # колесико вниз
                        if event.button == 4:
                            # удобный прием для закольцованной прокрутки
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        # колесико вверх
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        # колесико вниз
                        if event.button == 4:
                            # удобный прием для закольцованной прокрутки
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        # колесико вверх
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_click = False
                    if event.button == 3:
                        self.right_click = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tm.save('map.json')
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.cam_speed += 1
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.cam_speed -= 1

                if event.type == pygame.KEYUP:
                    # если клавиша(ы) отпущена(ы)
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            # управление камерой
            self.camera_position[0] += (self.movement[1] - self.movement[0]) * self.cam_speed
            self.camera_position[1] += (self.movement[3] - self.movement[2]) * self.cam_speed

            # отрисовываем фон, платформы, врагов и собираемые предметы
            self.display.blit(self.background, (0, 0))

            # логика LevelEditor
            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            self.tm.render(self.display, self.camera_position)
            self.display.blit(current_tile_image, (5, 5))

            mousepos = pygame.mouse.get_pos()
            mousepos = (mousepos[0] / RENDER_SCALE, mousepos[1] / RENDER_SCALE)
            tile_pos = (int((mousepos[0] + self.camera_position[0]) // self.tm.size),
                        int((mousepos[1] + self.camera_position[1]) // self.tm.size))

            if self.ongrid:
                self.display.blit(current_tile_image, (tile_pos[0] * self.tm.size - self.camera_position[0],
                                                       tile_pos[1] * self.tm.size - self.camera_position[1]))
            else:
                self.display.blit(current_tile_image, mousepos)

            if self.left_click and self.ongrid:
                self.tm.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = Tile(type=self.tile_list[self.tile_group],
                                                                                  variant=self.tile_variant,
                                                                                  position=tile_pos)

            if self.right_click:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tm.tilemap:
                    del self.tm.tilemap[tile_loc]
                for tile in self.tm.offgrid_tiles.copy():
                    tile_image = self.assets[tile.type][tile.variant]
                    tile_r = pygame.Rect(tile.position[0] - self.camera_position[0],
                                         tile.position[1] - self.camera_position[1], tile_image.get_width(),
                                         tile_image.get_height())
                    if tile_r.collidepoint(mousepos):
                        self.tm.offgrid_tiles.remove(tile)

            # отрисовка положения курсора
            fps_text = pygame.font.Font(None, 24).render(
                f'{mousepos[0] + self.camera_position[0], mousepos[1] + self.camera_position[1]}', False,
                (255, 255, 255))
            self.display.blit(fps_text, (self.display.get_width() - 160, 50))

            # обновление экрана и установка частоты кадров
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()


editor = LevelEditor()
editor.run()
