import pygame
from dotenv import load_dotenv
from random import choice
from tile import Tile
from player import Player
from weapon import Weapon
from debug import debug
import support
import settings
from ui import UI

load_dotenv()


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        self.create_map()

        # User interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': support.import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': support.import_csv_layout('../map/map_Grass.csv'),
            'object': support.import_csv_layout('../map/map_Objects.csv')
        }

        graphics = {
            'grass': support.import_folder('../graphics/grass'),
            'objects': support.import_folder('../graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * int(settings.TILESIZE)
                        y = row_index * int(settings.TILESIZE)

                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.obstacles_sprites, self.visible_sprites], 'grass', random_grass_image)

        self.player = Player(
            (1920, 1310), [self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        # debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground_limpo.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
