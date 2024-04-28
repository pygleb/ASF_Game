import pygame
import json


class Tilemap:
    def __init__(self, game, tile_size=32):
        self.game = game
        self.size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def render(self, screen, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            screen.blit(self.game.assets[tile.type][tile.variant],
                        (tile.position[0] - offset[0], tile.position[1] - offset[1]))

        for tile in self.tilemap:
            tile = self.tilemap[tile]
            screen.blit(self.game.assets[tile.type][tile.variant],
                        (tile.position[0] * self.size - offset[0], tile.position[1] * self.size - offset[1]))

    def getrects(self):
        rects = []
        for tile in self.tilemap:
            tile = self.tilemap[tile]
            rects.append(pygame.Rect(tile.position[0] * self.size, tile.position[1] * self.size, self.size, self.size))
        return rects

    # оптимизация, обработка только ближайших тайлов
    def physics_rects_around(self, pos):
        pass

    def save(self, path):
        f = open(path, 'w')

        data = {
            'tilemap': {str(position): tile.__dict__() for position, tile in self.tilemap.items()},
            'size': self.size,
            'offgrid': [tile.__dict__() for tile in self.offgrid_tiles]
        }

        json.dump(data, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        level_data = json.load(f)
        f.close()

        self.tilemap = {}
        self.size = level_data['size']
        self.offgrid_tiles = []

        for position_str, tile in level_data['tilemap'].items():
            self.tilemap[position_str] = Tile(tile['type'], tile['variant'], tile['position'])

        for tile_data in level_data['offgrid']:
            self.offgrid_tiles.append(Tile(tile_data['type'], tile_data['variant'], tile_data['position']))


class Tile:
    def __init__(self, type, variant, position):
        self.type = type
        self.variant = variant
        self.position = position

    def __dict__(self):
        return {'type': self.type, 'variant': self.variant, 'position': self.position}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)