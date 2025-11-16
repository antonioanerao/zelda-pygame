import pygame
from dotenv import load_dotenv
import settings

load_dotenv()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((int(settings.TILESIZE), int(settings.TILESIZE)))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - int(settings.TILESIZE)))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 10)
