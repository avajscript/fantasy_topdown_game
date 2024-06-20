import sys

import pygame as pg

pg.init()
pg.mixer.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
    def __init__(self):
        super(Player, self).__init__()
        self.player_images = player_images
        self.player_images[0].iter()
        self.player_action_images = player_actions
        self.point = (0, 0)
        self.image = player_images[0].next()
        self.image_row = player_images[0]
        self.current_key = 0
    def update(self, pressed_keys):
        if self.current_key != K_UP and (pressed_keys[K_UP] or pressed_keys[K_w]):
            self.current_key = K_UP
            self.image_row = self.player_images[player_anim_dict["upWalk"]]
            self.image = self.image_row.iter().next()
        elif self.current_key != K_RIGHT and (pressed_keys[K_RIGHT] or pressed_keys[K_d]):
            self.current_key = K_RIGHT
            self.image_row = self.player_images[player_anim_dict["rightWalk"]]
            self.image = self.image_row.iter().next()
        elif self.current_key != K_DOWN and (pressed_keys[K_DOWN] or pressed_keys[K_s]):
            self.current_key = K_DOWN
            self.image_row = self.player_images[player_anim_dict["downWalk"]]
            self.image = self.image_row.iter().next()
        elif self.current_key != K_LEFT and (pressed_keys[K_LEFT] or pressed_keys[K_a]):
            self.current_key = K_LEFT
            self.image_row = self.player_images[player_anim_dict["leftWalk"]]
            self.image = self.image_row.iter().next()
        # else:


    def stop(self, key):

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
        screen.blit(self.image, (0, 0))


running = True

# n = 0
# player_images[n].iter()
# image = player_images[n].next()

player = Player()

while running:
    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
        elif e.type == pg.KEYDOWN:
            pressed_keys = pg.key.get_pressed()
            if (pressed_keys[K_UP] or pressed_keys[K_w] or pressed_keys[K_RIGHT] or pressed_keys[K_d]
                    or pressed_keys[K_DOWN] or pressed_keys[K_s] or pressed_keys[K_LEFT] or pressed_keys[K_a]):
                player.update(pressed_keys)
        elif e.type == pg.KEYUP:
            if (e.key == K_UP or e.key == K_w or e.key == K_RIGHT or e.key == K_d
                    or e.key == K_DOWN or e.key == K_s or e.key == K_LEFT or e.key == K_a):
                player.stop(e.key)

    screen.fill((0, 0, 0))
    player.draw(screen)
    pg.display.flip()
    clock.tick(FPS)