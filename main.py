import copy
import string
import sys
from typing import List

import pygame as pg
import pytmx
from pytmx.util_pygame import load_pygame
import constants
from classes.Tile import Tile
from classes.Interactable_Objects import InteractableObject, Chest
from classes.TileUtility import TileUtility
from spritesheet import AnimationList
from enum import Enum

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
map_one_tmx = load_pygame("graphics/main_map.tmx")

# get layers
# for layer in map_one_tmx.visible_layers:
#     print(layer)

# Constants

# Enums


from classes.Inventory import Inventory, InventoryDrawing, Item

from images import (player_images, player_actions,
                    door_animation, chest_animation,
                    inventory_img, inventory_row_horizontal_img, inventory_slot_img,
                    )
from spritesheet import AnimationList

from pygame.locals import (
    K_UP,
    K_RIGHT,
    K_DOWN,
    K_LEFT,
    K_w,
    K_d,
    K_s,
    K_a,
    K_q,
    K_e,
    K_SPACE,  # Object interaction button
    K_ESCAPE,
    K_RETURN,
    QUIT,
    KEYDOWN,
    KEYUP,
    RLEACCEL
)

# special action keys that caused a player event
ACTION_KEYS = [K_SPACE, K_q, K_e]
MOVEMENT_KEYS = [K_w, K_d, K_s, K_a, K_UP, K_RIGHT, K_DOWN, K_LEFT]


animations_dict = {
}


animations_dict["door"] = door_animation

animations_dict["chest"] = chest_animation

animations = []
running_animation_names = []
loaded_files = []
# The list interactable objects to be drawn on the screen. Chests and such.
interactable_objects = pg.sprite.Group()


def door_animation(x, y):
    animations_dict["door"].x = x * constants.TILE_WIDTH
    animations_dict["door"].y = y * constants.TILE_WIDTH

    # animations_dict.iter()
    animations.append(animations_dict["door"])


def chest_animation(x, y):
    animations_dict["chest"].x = x * constants.TILE_WIDTH
    animations_dict["chest"].y = y * constants.TILE_WIDTH
    # animations_dict.iter()
    animations.append(animations_dict["chest"])


def open_chest(tile: Tile, items: string, coords: tuple):
    """
    Creates a chest object and adds it to the list of interactable_objects, which will be drawn in the game loop
    It will be removed when the user closes it
    :param items: List of items to be added to the chest
    :param coords: the coordinates (x, y) to draw the chest
    :return:
    """
    chest: Chest = Chest(tile=tile, items=items, chest_image=inventory_img, x=coords[0]+1, y=coords[1])

    chest.redraw_images()
    interactable_objects.add(chest)


def delete_interactable_objects():
    interactable_objects.empty()


function_dict = {
    "door": door_animation,
    "chest": chest_animation,
    "openchest": open_chest
}


class GameMap:
    def __init__(self):
        self.tile_array = [[None for _ in range(constants.GAME_WIDTH_TILES + 1)] for _ in range(constants.GAME_HEIGHT_TILES + 1)]
        self.sprite_group = pg.sprite.Group()
    def get_tiles(self, tile_sprite):
        sprite_collisions = []
        for sprite in pg.sprite.spritecollide(tile_sprite, self.sprite_group, False):
            sprite_collisions.append(sprite)
        return sprite_collisions


# x, y coordinates that match the tile in that position [50][40]


layers = map_one_tmx.layers
game_map = GameMap()
for layer_idx, layer in enumerate(layers):
    # Iterate over object layer
    if isinstance(layer, pytmx.TiledObjectGroup):
        for obj in layer:
            x, y = int(obj.x/constants.TILE_WIDTH), int(obj.y/constants.TILE_WIDTH)
            pos = (x * constants.TILE_WIDTH, y * constants.TILE_WIDTH)
            tile = Tile(pos=pos, surf=obj.image, groups=game_map.sprite_group, properties=obj.properties, coords=(x, y))
            game_map.tile_array[x][y] = tile
    # Iterate over tile layers
    elif hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            properties = map_one_tmx.get_tile_properties(x, y, layer_idx)
            pos = (x * constants.TILE_WIDTH, y * constants.TILE_WIDTH)
            tile = Tile(pos=pos, surf=surf, groups=game_map.sprite_group, properties=properties, coords=(x, y))
            game_map.tile_array[x][y] = tile

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

    "down_sword": 8,
    "right_sword": 9,
    "up_sword": 10,
    "left_sword": 11,

    "rightCrawl": 12,
    "leftCrawl": 13,

    "down_pickaxe": 14,
    "right_pickaxe": 15,
    "up_pickaxe": 16,
    "left_pickaxe": 17,

    "down_hatchet": 18,
    "right_hatchet": 19,
    "up_hatchet": 20,
    "left_hatchet": 21,

    "down_hoe": 22,
    "right_hoe": 23,
    "up_hoe": 24,
    "left_hoe": 25,

    "down_water": 26,
    "right_water": 27,
    "up_water": 28,
    "left_water": 29
}


class Game:
    def __init__(self, inventory):
        self.inventory_draw_state: InventoryDrawing = InventoryDrawing.FULL_INVENTORY
        self.inventory: Inventory = inventory
    def draw(self, screen):
        inventory.draw(screen, self.inventory_draw_state)


class Player(pg.sprite.Sprite):
    def __init__(self, player_inv: Inventory, x, y):
        super(Player, self).__init__()
        self.inv = player_inv
        self.pos = pg.math.Vector2(x * constants.TILE_WIDTH, y * constants.TILE_WIDTH)
        # x, y
        self.dirvec = pg.math.Vector2(0, 0)
        self.new_pos = [x * constants.TILE_WIDTH, y * constants.TILE_WIDTH]
        self.point = pg.math.Vector2(x, y)
        self.player_images = player_images
        self.player_images[0].iter()
        self.player_action_images = player_actions
        self.image = player_images[0].next()
        self.image_row = player_images[0]
        self.prev_motion_row = player_images[0]
        self.current_keys = (0, 0)
        self.keys_pressed = []

    def get_dir_string(self):
        """
        Gets the string value of the direction the player is facing
        :return: The direction the player is currently facing
        :rtype: str
        """
        direction = None
        if self.dirvec[0] != 0:
            if self.dirvec[0] > 0:
                direction = "right"
            else:
                direction = "left"
        else:
            if self.dirvec[1] > 0:
                direction = "down"
            else:
                direction = "up"

        return direction

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
                new_point_tile = game_map.tile_array[int(new_point.x)][int(new_point.y)]
                # Exit function and do nothing if the next tile doesn't exit
                if new_point_tile is None:
                    return
                # If player can't move through tile
                if not new_point_tile.properties['traversable']:
                    # For tiles that walking into causes an interaction
                    if 'movement_interactable' in new_point_tile.properties:
                        if new_point_tile.properties['movement_interactable']:
                            interaction_type = new_point_tile.properties['interaction_type']
                            # Performs a function based on the corresponding tile location and tile type
                            if interaction_type in running_animation_names:
                                return
                            function_dict[interaction_type](new_point.x, new_point.y)
                            running_animation_names.append(interaction_type)
                    # Exit
                    return
                self.point = new_point
                # Set new x coordinate position
                new_pos = pg.math.Vector2(self.dirvec[0] * constants.TILE_WIDTH, self.dirvec[1] * constants.TILE_WIDTH)
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
            self.prev_motion_row = self.image_row
        self.keys_pressed = [key_press for key_press in self.keys_pressed if key_press != key_to_remove]

    def detect_hide_interactable_objects(self):
        """
        Checks if the tile the player is moving onto is the current interactable object (chest, etc)
        If not, then delete all interactable objects.
        This means the player moved away from the interaction, so we should hide it from the screen.
        :return: None
        """
        new_point = self.point + self.dirvec
        new_point_tile: Tile = game_map.tile_array[int(new_point.x)][int(new_point.y)]
        print(new_point_tile.properties)
        print(type(new_point_tile.properties))
        if "action_interactable" in new_point_tile.properties:
            if new_point_tile.properties["action_interactable"] is not True:
                delete_interactable_objects()
        else:
            delete_interactable_objects()


    def action_event(self, key):
        if key == K_q:
            pass
        elif key == K_e:
            pass
            # Perform the interaction based on the tile in front of the player
        elif key == K_SPACE:
            print("inventor")
            equipped_item: string = player.inv.get_equipped_item_name()
            direction: string = self.get_dir_string()
            if direction is not None and equipped_item is not None:
                print("dir string")
                print(direction + "_" + equipped_item)
                self.image_row = self.player_images[player_anim_dict[direction + "_" + equipped_item]]
            # get the tile the player is interacting with (in front of him)
            new_point = self.point + self.dirvec
            new_point_tile: Tile = game_map.tile_array[int(new_point.x)][int(new_point.y)]
            if "actioned" in new_point_tile.properties:
                if new_point_tile.properties['actioned']:
                    if new_point_tile.properties['interaction_type'] == 'chest':
                        # Open the chest display with the tile object properties
                        function_dict["openchest"](new_point_tile, new_point_tile.properties['items'], new_point_tile.coords)

                # Run the first animation of the interactable object
                elif "action_interactable" in new_point_tile.properties:
                    interaction_type = new_point_tile.properties['interaction_type']
                    # Interaction animation is already running, so don't run it
                    # Most likely due to rapid double click
                    if interaction_type in running_animation_names:
                        return
                    function_dict[interaction_type](new_point.x, new_point.y)
                    running_animation_names.append(interaction_type)

    def draw(self, screen):
        try:
            self.image = self.image_row.next()
        except:
            self.image_row = self.prev_motion_row
            self.image = self.image_row.next()
        screen.blit(self.image, (self.pos[0] - constants.TILE_WIDTH / 2, self.pos[1] - constants.TILE_WIDTH / 2))


running = True

# n = 0
# player_images[n].iter()
# image = player_images[n].next()


inventory = Inventory(inventory_img, inventory_row_horizontal_img, inventory_slot_img)
player = Player(inventory, 6, 5)
game = Game(inventory)


def draw_grid_lines():
    for x in range(0, constants.SCREEN_WIDTH, constants.TILE_WIDTH):
        pg.draw.line(screen, (255, 0, 0), (x, 0), (x, constants.SCREEN_HEIGHT))
    for y in range(0, constants.SCREEN_HEIGHT, constants.TILE_WIDTH):
        pg.draw.line(screen, (255, 0, 0), (0, y), (constants.SCREEN_WIDTH, y))


while running:
    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
        elif e.type == pg.KEYDOWN:
            pressed_keys = pg.key.get_pressed()
            # Player movement
            if e.key in MOVEMENT_KEYS:
                player.press_key(pressed_keys)
                if len(interactable_objects) > 0:
                    player.detect_hide_interactable_objects()
            # Player action
            elif e.key in ACTION_KEYS:
                player.action_event(e.key)
        # Key release
        elif e.type == pg.KEYUP:
            if e.key in MOVEMENT_KEYS:
                player.release_key(e.key)
        # Mouse press
        elif e.type == pg.MOUSEBUTTONDOWN:
            # Left mouse button press
            if e.button == 1:
                # Check for collisions between all interactable objects
                mouse_pos = pg.mouse.get_pos()
                mouse_pos_sprite: pg.sprite.Sprite = pg.sprite.Sprite
                mouse_pos_sprite.rect = pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
                collisions = pg.sprite.spritecollide(mouse_pos_sprite, interactable_objects, False)
                # Perform the click action on the interactable object
                for int_obj in collisions:
                    [item, chest_tile] = int_obj.click_action(mouse_pos[0], mouse_pos[1])
                    # If user clicked an empty chest slot, this will return none
                    if item is not None:
                        inventory.loot_item(item)
                        print("item")
                        print(item)
                        TileUtility.remove_item(chest_tile, item)

    player.update()
    game_map.sprite_group.draw(screen)
    # Draw all the animations, update the screen to the last image in the animation
    for a in running_animation_names:
        pass
    try:
        # Perform animation actions on each animation
        for animation in animations:
            # Create a sprite to compare to the sprite group
            tile_sprite = pg.sprite.Sprite
            tile_sprite.rect = pg.rect.Rect(animation.x, animation.y, constants.TILE_WIDTH, constants.TILE_WIDTH)
            # Get list of sprite collisions. Layers are stacked on top of each other, so there will be multiple.
            # Top tile should always be the interaction object final state image
            sprite_collisions = game_map.get_tiles(tile_sprite)
            last_sprite = sprite_collisions[len(sprite_collisions) - 1]
            last_sprite.image = animation.images[animation.count - 1]
            screen.blit(sprite_collisions[len(sprite_collisions) - 2].image, tile_sprite.rect)
            screen.blit(animation.next(), (animation.x, animation.y))
    # Once the animation is done with all frames, it throws exception and ends up here
    except:
        # Delete animation
        animations.remove(animation)
        # Reset animation for next time its called
        animation.iter()
        running_animation_names.remove(animation.name)
        # Make it so user can walk through the object. Used for doors and other objects that cause an
        # animation to walk through
        if "movement_interactable" in last_sprite.properties:
            last_sprite.properties['traversable'] = True
        # Set tile to actioned, which means the space button was pressed and the first action was performed on the object
        # Typically used for chests, and such
        if "action_interactable" in last_sprite.properties:
            if "actioned" in last_sprite.properties:
                last_sprite.properties['actioned'] = True

    player.draw(screen)
    interactable_objects.draw(screen)
    game.draw(screen)
    #draw_grid_lines()

    pg.display.flip()
    clock.tick(FPS)
