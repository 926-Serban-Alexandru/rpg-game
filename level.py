import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        # sprite group
        self.visible_sprites = YCameraClass()
        self.obstacle_sprites = pygame.sprite.Group()
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # draw ze game
        self.visible_sprites.custom_draw(self.player)  # replced the old draw with custom_draw.No need for self.display_surface
        # it was declared in the custom class
        self.visible_sprites.update()


class YCameraClass(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.y = player.rect.centery - self.half_height #the offsets
        self.offset.x = player.rect.centerx - self.half_width

        #for sprite in self.sprites(): we do it sorted by y cuz some sprites are above the player and some are below
        #creates a weird situation where the player is behind a rock/obstacle when it shouldn't be
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
