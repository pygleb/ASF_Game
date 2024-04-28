################################################################
# При запуске:                                                  #
# синие элементы - платформы,                                  #
# красный элемент - враг,                                      #
# зеленый элемент - игрок,                                     #
# желтый элемент - собираемый предмет                          #
#                                                              #
# Управление: стрелки клавиатуры для движения, пробел для прыжка#
################################################################

# Для запуска редактора уровней запустите level_editor.py

# подключние бибилиотек
from scripts.entities.static_object import Platform, Collectible
from scripts.entities.updatable_objects import Enemy
from scripts.entities.physics_objects import PhysicsObject
from scripts.tilemap import Tilemap
from scripts.utils import *
#from scripts.entities.Healt import *

# константы-параметры окна
WIDTH = 800
HEIGHT = 600
D_WIDTH = 800
D_HEIGHT = 600
# константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
# прочие константы
JUMP_FORCE = 8


class Game:
    def __init__(self):
        # инициализация Pygame
        self.collision_objects = []
        pygame.init()

        # инициализация движения
        self.movement = [False, False]

        # создаем экран + дисплей, счетчик частоты кадров и очков
        pygame.display.set_caption('ASF')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((D_WIDTH, D_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0

        # подгружаем текстуры
        self.assets = {
            'player': load_image('player.png'),
            'background': load_image('background.png'),
            'heart': load_image('heart.png'),
            # тайлы
            'testblock': load_tileset('testblock'),
            'background-tiles': load_tileset('background'),
            'interior_walls_1': load_tileset('interior_walls_1')
            # 'platform': load_image('platform.png'),
            # 'enemy': load_image('enemy.png'),
            # 'collectible': load_image('collectible.png')
        }

        # создаем карту из тайлмапа
        self.tm = Tilemap(self)
        self.tm.load('map.json')

        # создаем игрока, платформы, врагов и то, что будем собирать в игре
        self.player = PhysicsObject(self, 'player', self.assets['player'], (275, 170))
        self.platforms_list = [Platform(self, 0, HEIGHT - 25, WIDTH, 50), Platform(self, 0, 0, 100, 20),
                               Platform(self, 100, 350, 100, 20),
                               Platform(self, 250, 170, 100, 20)]
        self.enemies_list = [Enemy(self, 120, 315),Enemy(self, 1086, 419),Enemy(self, 2688, 450), Enemy(self, 3934, 348)]
        self.win=4124
        self.collectibles_list = [Collectible(self, self.win, 475)]
        self.enemy_len = 4
        # счёт игры
        self.font = pygame.font.Font(None, 36)  # создание объекта, выбор размера шрифта
        self.score_text = self.font.render("Счёт: 0", True, BLACK)  # выбор цвета и текст
        self.score_rect = self.score_text.get_rect()  # создание хитбокса текста
        self.score_rect.topleft = (WIDTH // 2, 100)  # расположение хитбокса\текста на экране

        # позиция камеры
        self.camera_position = [0, 0]

        # загружаем фон
        self.background = pygame.transform.scale(self.assets['background'], (WIDTH, HEIGHT))

        # игровой цикл
        self.running = True


        self.player_healt = 3

    # основной игровой цикл
    def run(self):
        while self.running:
            #смерть при падении
            if self.player.pos[1]>1000: pygame.quit ()
            if self.player.pos[0]>self.win:
                print("Winner")
                self.running = False
            if self.player_healt < 1:
                print("lose")
                self.running = False
            for i in range(self.enemy_len):
                if (self.player.pos[0] == self.enemies_list[i].rect[0]): self.player_healt -= 1

            # проверка ввода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    # если клавиша(ы) нажата(ы)
                    # увеличивает скорость передвижения и высоту прыжка при зажатом шифт
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        self.RUN = 2
                        self.Jump_factor = 1.2
                    else:
                        self.RUN = 1
                        self.Jump_factor = 1
                    # перемещение по горизронтали
                    if pygame.key.get_pressed()[pygame.K_LEFT]:
                        self.movement[0] = True * self.RUN
                    if pygame.key.get_pressed()[pygame.K_RIGHT]:
                        self.movement[1] = True * self.RUN
                    # прыжок при наличии поверхности для отталкивания
                    if event.key == pygame.K_SPACE and self.player.on_ground == True:
                        self.player.velocity[1] = -JUMP_FORCE * self.Jump_factor
                        self.player.on_ground = False
                        self.Double_jump_flag = True
                        self.Tick_1_jump = pygame.time.get_ticks()
                    # двойной прыжок после первого по прошествии 0.5 секунды
                    if event.key == pygame.K_SPACE and (
                            self.Double_jump_flag == True) and pygame.time.get_ticks() - self.Tick_1_jump > 200:
                        self.player.velocity[1] = -JUMP_FORCE * self.Jump_factor
                        self.Double_jump_flag = False
                    # пикирование
                    if event.key == pygame.K_LCTRL:
                        self.player.velocity[1] = JUMP_FORCE * 3
                if event.type == pygame.KEYUP:
                    # если клавиша(ы) отпущена(ы)
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # отрисовываем фон, платформы, врагов и собираемые предметы
            self.display.blit(self.background, (0, 0))
            # self.platforms.draw(self.display)
            # self.enemies.draw(self.display)
            # self.collectibles.draw(self.display)

            # обновляем значения атрибутов всех объектов
            for i in self.enemies_list:
                i.update()
                i.render(self.display, self.camera_position)
            for i in self.platforms_list:
                i.render(self.display, self.camera_position)
            for i in self.collectibles_list:
                i.render(self.display, self.camera_position)

            # отрисовываем тайлы
            self.tm.render(self.display, offset=self.camera_position)

            # обновляем игрока
            # collision object - объект с полем rect
            self.collision_objects_rects = []
            self.collision_objects_rects.extend(self.tm.getrects())
            for p in self.platforms_list:
                self.collision_objects_rects.append(p.rect)

            self.player.update(self.collision_objects_rects, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.camera_position)

            # двигаем камеру
            self.camera_position[0] += (self.player.getrect().centerx - self.display.get_width() / 2 -
                                        self.camera_position[0]) / 30
            self.camera_position[1] += (self.player.getrect().centery - self.display.get_height() / 2 -
                                        self.camera_position[1]) / 30

            # обновление счёта на экране
            score_text = self.font.render("Счёт: " + str(self.score), True, BLACK)
            self.display.blit(score_text, self.score_rect)

            # отрисовываем сердечки
            self.assets['heart'] = pygame.transform.scale(self.assets['heart'],(60,60)).convert_alpha()
            for i in range(0,65*self.player_healt,65):
                self.display.blit(self.assets['heart'], (i, 5))

            # обновление экрана и установка частоты кадров
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


game = Game()
game.run()
