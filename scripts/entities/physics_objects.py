from scripts.entities.static_object import StaticObject

# Физические константы
max_fall_velocity = 1000


# описывает поведение каждого объекта, который может быть подвергнут
# гравитационному воздействию
class PhysicsObject(StaticObject):
    # функция, обновляющая физический объект
    def update(self, collision_objects_rects, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] * 4 + self.velocity[0], movement[1] + self.velocity[1])

        # проверка объектов с rect на коллизию по горизонтали
        self.pos[0] += frame_movement[0]
        entity_rect = self.getrect()
        for rect in collision_objects_rects:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    #TODO:  перезарядка прыжка при касании стены                                    self.on_ground = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    #TODO:  перезарядка прыжка при касании стены                                    self.on_ground = True
                self.pos[0] = entity_rect.x

        # проверка объектов с rect на коллизию по вертикали
        self.pos[1] += frame_movement[1]
        entity_rect = self.getrect()
        for rect in collision_objects_rects:
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.on_ground=True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(max_fall_velocity, self.velocity[1] + 0.25)

        # останавливаем объект при наличии коллизии сверху или снизу
        # по вертикали
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    # функция, отрисовывающая физический объект
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.image_asset, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
