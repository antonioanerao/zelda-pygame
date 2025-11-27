import pygame
import settings


class UI:
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(settings.UI_FONT, settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, settings.HEALTH_BAR_WIDTH, settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, settings.ENERGY_BAR_WIDTH, settings.BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, color, bg_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, settings.HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, settings.ENERGY_COLOR)
