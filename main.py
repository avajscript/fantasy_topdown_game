import sys
import pygame as pg
from pytmx.util_pygame import load_pygame

pg.init()
pg.mixer.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
map_one_tmx = load_pygame("graphics/main_map.tmx")

# get layers
# for layer in map_one_tmx.visible_layers:
#     print(layer)

# Constants
TILE_WIDTH = 16

from images import player_images, player_actions

from pygame.locals import (
    K_UP,
    K_RIGHT,
    K_DOWN,
    K_LEFT,
    K_w,
    K_d,
    K_s,
    K_a,
    K_ESCAPE,
    K_RETURN,
    QUIT,
    KEYDOWN,
    KEYUP,
    RLEACCEL
)

layers = map_one_tmx.visible_layers


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

sprite_group = pg.sprite.Group()

for layer in layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * TILE_WIDTH, y * TILE_WIDTH)
            Tile(pos=pos, surf=surf, groups=sprite_group)



clock = pg.time.Clock()
FPS = 60

player_anim_dict = {
    "down": 0,
    "right": 1,
    "up": 2,
    "left": 3,
    "downWalk": 4,
    "rightWalk": 5,
    "upWalk": 6,
    "leftWalk": 7,
    "downAttack": 8,
    "rightAttack": 9,
    "upAttack": 10,
    "leftAttack": 11,
    "rightCrawl": 12,
    "leftCrawl": 13
}


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.player_images = player_images
        self.player_images[0].iter()
        self.player_action_images = player_actions
        self.point = (0, 0)
        self.image = player_images[0].next()
        self.image_row = player_images[0]
        self.current_keys = (0, 0)
        self.moving_timer = pg.time.get_ticks()

    def press_key(self, pressed_keys):
        if self.current_keys[1] != K_UP and (pressed_keys[K_UP] or pressed_keys[K_w]):
            self.current_keys = (K_a, K_UP)
            self.image_row = self.player_images[player_anim_dict["upWalk"]]
            self.image = self.image_row.iter()
        elif self.current_keys[1] != K_RIGHT and (pressed_keys[K_RIGHT] or pressed_keys[K_d]):
            self.current_keys = (K_d, K_RIGHT)
            self.image_row = self.player_images[player_anim_dict["rightWalk"]]
            self.image = self.image_row.iter()
        elif self.current_keys[1] != K_DOWN and (pressed_keys[K_DOWN] or pressed_keys[K_s]):
            self.current_keys = (K_s, K_DOWN)
            self.image_row = self.player_images[player_anim_dict["downWalk"]]
            self.image = self.image_row.iter()
        elif self.current_keys[1] != K_LEFT and (pressed_keys[K_LEFT] or pressed_keys[K_a]):
            self.current_keys = (K_a, K_LEFT)
            self.image_row = self.player_images[player_anim_dict["leftWalk"]]
            self.image = self.image_row.iter()


    def update(self):

    def release_key(self, key):
        # Check to see if key is the currently pressed key being released.
        # Then set the walking speed
        if key == self.current_keys[0] or key == self.current_keys[1]:
            # Reset keys to none being pressed
            self.current_keys = (0, 0)
            if key == K_UP or key == K_w:
                self.image_row = self.player_images[player_anim_dict["up"]]
            elif key == K_RIGHT or key == K_d:
                self.image_row = self.player_images[player_anim_dict["right"]]
            elif key == K_DOWN or key == K_s:
                self.image_row = self.player_images[player_anim_dict["down"]]
            elif key == K_LEFT or key == K_a:
                self.image_row = self.player_images[player_anim_dict["left"]]

    # if self.image_row == self.player_images[player_anim_dict["upWalk"]]:
    #         self.image_row = self.player_images[player_anim_dict["up"]]
    #     elif self.image_row == self.player_images[player_anim_dict["rightWalk"]]:
    #         self.image_row = self.player_images[player_anim_dict["right"]]
    #     elif self.image_row == self.player_images[player_anim_dict["downWalk"]]:
    #         self.image_row = self.player_images[player_anim_dict["down"]]
    #     elif self.image_row == self.player_images[player_anim_dict["leftWalk"]]:
    #         self.image_row = self.player_images[player_anim_dict["left"]]
    def draw(self, screen):
        self.image = self.image_row.next()
        screen.blit(self.image, (self.x * TILE_WIDTH, self.y * TILE_WIDTH))


running = True

# n = 0
# player_images[n].iter()
# image = player_images[n].next()

player = Player(0, 0)


while running:
    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
        elif e.type == pg.KEYDOWN:
            pressed_keys = pg.key.get_pressed()
            if (pressed_keys[K_UP] or pressed_keys[K_w] or pressed_keys[K_RIGHT] or pressed_keys[K_d]
                    or pressed_keys[K_DOWN] or pressed_keys[K_s] or pressed_keys[K_LEFT] or pressed_keys[K_a]):
                player.press_key(pressed_keys)
        elif e.type == pg.KEYUP:
            print("e")
            print(e)
            if (e.key == K_UP or e.key == K_w or e.key == K_RIGHT or e.key == K_d
                    or e.key == K_DOWN or e.key == K_s or e.key == K_LEFT or e.key == K_a):
                player.release_key(e.key)

    sprite_group.draw(screen)
    player.draw(screen)
    pg.display.flip()
    clock.tick(FPS)
