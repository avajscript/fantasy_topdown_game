import pygame as pg
import copy
from spritesheet import Spritesheet, SpriteStripAnim
import os
path = "graphics/Cute_Fantasy"
split_tiles_path = "graphics/split_tiles"
FPS = 60
frames = FPS / 10
player_images = [
    # Walking
    # down - 0
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 0, 32, 32), 6, -1, True, frames),
    # right - 1
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 32, 32, 32), 6, -1, True, frames),
    # up - 2
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 64, 32, 32), 6, -1, True, frames),
    # left - 3
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 32, 32, 32), 6, -1, True, frames).flip_images(),

    # Running
    # down run - 4
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 96, 32, 32), 6, -1, True, frames),
    # right run - 5
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 128, 32, 32), 6, -1, True, frames),
    # up run - 6
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 160, 32, 32), 6, -1, True, frames),
    # left run - 7
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 128, 32, 32), 6, -1, True, frames).flip_images(),

    # Attacking
    # attack down - 8
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 192, 32, 32), 4, -1, False, frames),
    # attack right - 9
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, -1, False, frames),
    # attack up - 10
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 384, 32, 32), 4, -1, False, frames),
    # attack left - 11
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, -1, False, frames).flip_images(),

    # Crawling
    # crawl right - 12
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, -1, True, frames),
    # crawl left - 13
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, -1, True, frames).flip_images(),

    # Mining
    # Mine down - 14
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 32, 32, 32), 5, -1, True, frames),
    # Mine right - 15
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 0, 32, 32), 5, -1, True, frames),
    # Mine up - 16
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 64, 32, 32), 5, -1, True, frames),
    # Mine left - 17
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 0, 32, 32), 5, -1, True, frames).flip_images(),

    # Chopping
    # Chop down - 18
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 128, 32, 32), 5, -1, True, frames),
    # Chop right - 19
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 96, 32, 32), 5, -1, True, frames),
    # Chop up - 20
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 160, 32, 32), 5, -1, True, frames),
    # Chop left - 21
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 96, 32, 32), 5, -1, True, frames).flip_images(),

    # Digging
    # Dig down - 22
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 224, 32, 32), 5, -1, True, frames),
    # Dig right - 23
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 192, 32, 32), 5, -1, True, frames),
    # Dig up - 24
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 256, 32, 32), 5, -1, True, frames),
    # Dig left - 25
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 192, 32, 32), 5, -1, True, frames).flip_images(),

    # Watering
    # Water down - 26
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 288, 32, 32), 5, -1, True, frames),
    # Water right - 27
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 352, 32, 32), 5, -1, True, frames),
    # Water right - 28
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 352, 32, 32), 5, -1, True, frames),
    # Water left - 29
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 352, 32, 32), 5, -1, True, frames).flip_images(),
]

player_actions = [
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 0, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 48, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 96, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 144, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 192, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 240, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 288, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 336, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 384, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 432, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 480, 48, 48), 2, 1, True, frames),
    SpriteStripAnim(os.path.join(path, "Player/Player_Actions.png"), (0, 528, 48, 48), 2, 1, True, frames),
]

door_animation = SpriteStripAnim(os.path.join(path, "House/Walls/Wood_Door_Anim.png"), (0, 0, 16, 16), 6, 1, False, frames, "door")
chest_animation = SpriteStripAnim(os.path.join(path, "House/Objects/Chest_Anim.png"), (0, 0, 16, 16), 6, 1, False, frames, "chest")

door_animation_images = [
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-0.png")).convert_alpha(),
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-1.png")).convert_alpha(),
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-2.png")).convert_alpha(),
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-3.png")).convert_alpha(),
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-4.png")).convert_alpha(),
    pg.image.load(os.path.join(split_tiles_path, "house/walls/Wood_Door_Anim-5.png")).convert_alpha(),
]

inventory_slot_img = pg.image.load(os.path.join(split_tiles_path, "inventory/InventorySlots-14.png"))
inventory_row_horizontal_img = pg.image.load(os.path.join(split_tiles_path, "inventory/InventorySlots-15.png"))
inventory_img = pg.image.load(os.path.join(split_tiles_path, "inventory/InventorySlots-5.png"))

# Tools
arrow_img = pg.image.load(os.path.join(split_tiles_path, "icons/arrow.png"))
axe_img = pg.image.load(os.path.join(split_tiles_path, "icons/axe.png"))
bow_img = pg.image.load(os.path.join(split_tiles_path, "icons/bow.png"))
hammer_img = pg.image.load(os.path.join(split_tiles_path, "icons/hammer.png"))
pickaxe_img = pg.image.load(os.path.join(split_tiles_path, "icons/pickaxe.png"))
sword_img = pg.image.load(os.path.join(split_tiles_path, "icons/sword.png"))
teapot_img = pg.image.load(os.path.join(split_tiles_path, "icons/teapot.png"))











