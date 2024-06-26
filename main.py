import sys
import pygame as pg
import pytmx
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
PLAYER_WALK_BUFFER = 200
GAME_WIDTH_TILES = 50
GAME_HEIGHT_TILES = 40


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

animations_dict = {
}

animations_dict["door"] = [
    map_one_tmx.get_tile_properties_by_gid(280),
    map_one_tmx.get_tile_properties_by_gid(281),
    map_one_tmx.get_tile_properties_by_gid(282),
    map_one_tmx.get_tile_properties_by_gid(283),
    map_one_tmx.get_tile_properties_by_gid(284),
    map_one_tmx.get_tile_properties_by_gid(285),
]


tile_array = [[None for _ in range(GAME_WIDTH_TILES + 1)] for _ in range(GAME_HEIGHT_TILES + 1)]

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, properties, coords):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.properties = properties
        self.coords = coords

sprite_group = pg.sprite.Group()

for layer_idx, layer in enumerate(layers):
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            #print(f"x: {x}, y: {y}, surf: {surf}")
            properties = map_one_tmx.get_tile_properties(x, y, layer_idx)
            pos = (x * TILE_WIDTH, y * TILE_WIDTH)
            #print("props")
            #print(properties)
            tile = Tile(pos=pos, surf=surf, groups=sprite_group, properties=properties, coords=(x, y))
            tile_array[x][y] = tile



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
        self.pos = pg.math.Vector2(x * TILE_WIDTH, y * TILE_WIDTH)
        self.dirvec = pg.math.Vector2(0, 0)
        self.new_pos = [x * TILE_WIDTH, y * TILE_WIDTH]
        self.point = pg.math.Vector2(x, y)
        self.player_images = player_images
        self.player_images[0].iter()
        self.player_action_images = player_actions
        self.image = player_images[0].next()
        self.image_row = player_images[0]
        self.current_keys = (0, 0)
        self.keys_pressed = []


    def press_key(self, pressed_keys):

        # Key up
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.keys_pressed.append("up")
            self.dirvec = pg.math.Vector2(0, -1)
            self.image_row = self.player_images[player_anim_dict["upWalk"]]
            self.image = self.image_row.iter()
        # Key right
        elif (pressed_keys[K_RIGHT] or pressed_keys[K_d]):
            self.keys_pressed.append("right")
            self.dirvec = pg.math.Vector2(1, 0)
            self.image_row = self.player_images[player_anim_dict["rightWalk"]]
            self.image = self.image_row.iter()
        # Key down
        elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.keys_pressed.append("down")
            self.dirvec = pg.math.Vector2(0, 1)
            self.image_row = self.player_images[player_anim_dict["downWalk"]]
            self.image = self.image_row.iter()
        # Key left
        elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.keys_pressed.append("left")
            self.dirvec = pg.math.Vector2(-1, 0)
            self.image_row = self.player_images[player_anim_dict["leftWalk"]]
            self.image = self.image_row.iter()


    def update(self):
        # Going left
        if self.new_pos[0] - self.pos[0] < 0:
            self.pos[0] -= 1
        # Going right
        elif self.new_pos[0] - self.pos[0] > 0:
            self.pos[0] += 1
        # Going up
        elif self.new_pos[1] - self.pos[1] < 0:
            self.pos[1] -= 1
        # Going down
        elif self.new_pos[1] - self.pos[1] > 0:
            self.pos[1] += 1
        # If still in movement
        if self.new_pos == self.pos:
            # If key is pressed
            if len(self.keys_pressed):
                new_point = self.point + self.dirvec
                new_point_tile = tile_array[int(new_point.x)][int(new_point.y)]
                if new_point_tile is None:
                    return
                print("tile")
                print(new_point_tile.properties)
                if not new_point_tile.properties['traversable']:
                    print("new point tile")
                    print(new_point_tile.properties)
                    print("player position")
                    print(self.pos)
                    print("player xy")
                    print(self.point)
                    return
                self.point = new_point
                print("point")
                print(self.point)
                # Set new x coordinate position
                new_pos = pg.math.Vector2(self.dirvec[0] * TILE_WIDTH, self.dirvec[1] * TILE_WIDTH)
                # Update the new position based on current player coordinates
                self.new_pos = self.new_pos + new_pos




    def release_key(self, key):
        key_to_remove = ""
        # Check to see if key is the currently pressed key being released.
        # Then set the walking speed
        if self.dirvec != (0, 0):
            if key == K_UP or key == K_w:
                self.image_row = self.player_images[player_anim_dict["up"]]
                key_to_remove = "up"
            elif key == K_RIGHT or key == K_d:
                self.image_row = self.player_images[player_anim_dict["right"]]
                key_to_remove = "right"
            elif key == K_DOWN or key == K_s:
                self.image_row = self.player_images[player_anim_dict["down"]]
                key_to_remove = "down"
            elif key == K_LEFT or key == K_a:
                self.image_row = self.player_images[player_anim_dict["left"]]
                key_to_remove = "left"
        self.keys_pressed = [key_press for key_press in self.keys_pressed if key_press != key_to_remove]
    def draw(self, screen):
        self.image = self.image_row.next()
        screen.blit(self.image, (self.pos[0] - TILE_WIDTH / 2, self.pos[1] - TILE_WIDTH / 2))


running = True

# n = 0
# player_images[n].iter()
# image = player_images[n].next()

player = Player(1, 1)

def draw_grid_lines():
    for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
        pg.draw.line(screen, (255, 0, 0), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_WIDTH):
        pg.draw.line(screen, (255, 0, 0), (0, y), (SCREEN_WIDTH, y))
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
            if (e.key == K_UP or e.key == K_w or e.key == K_RIGHT or e.key == K_d
                    or e.key == K_DOWN or e.key == K_s or e.key == K_LEFT or e.key == K_a):
                player.release_key(e.key)

    player.update()
    sprite_group.draw(screen)

    player.draw(screen)
    draw_grid_lines()

    pg.display.flip()
    clock.tick(FPS)
