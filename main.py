import sys
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import Entity, Player
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pacman')
        self.screen = pygame.display.set_mode((1000, 800))
        self.display = pygame.Surface((500, 400))
        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]

        self.assets = {
            'wall': load_images('tiles/wall'),
            'floor': load_images('tiles/floor'),
            'player': load_image('entities/player/00_player.png'),
            'player/horizontal': Animation(load_images('entities/player/horizontal'), img_dur=8),
            'player/vertical': Animation(load_images('entities/player/vertical'), img_dur=8),
        }

        self.player = Player(self, (240, 100), (30, 30))
        self.speed = 2
        self.tilemap = Tilemap(self, tile_size=30)
        try:
            self.tilemap.load('assets/maps/map.json')
        except FileNotFoundError:
            pass

    def run(self):
        # -- Game Loop --
        while True:
            self.display.fill((0, 0, 0))

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * self.speed, (self.movement[3] - self.movement[2]) * self.speed))
            self.player.render(self.display)

            for event in pygame.event.get():
                # -- Exit Game --
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # -- Key Down --        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True

                # -- Key Up --
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                     
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()