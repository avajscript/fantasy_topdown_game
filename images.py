import pygame as pg
import copy
from spritesheet import Spritesheet, SpriteStripAnim
import os
path = r"C:\Users\matth\Documents\gamedev\fantasy\graphics\Cute_Fantasy_Free"
FPS = 60
frames  = FPS / 10
player_images = [
    # down
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 0, 32, 32), 6, 1, True, frames),
    # right
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 32, 32, 32), 6, 1, True, frames),
    # up
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 64, 32, 32), 6, 1, True, frames),
    # left
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 32, 32, 32), 6, 1, True, frames).flip_images(),
    # down run
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 96, 32, 32), 6, 1, True, frames),
    # right run
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 128, 32, 32), 6, 1, True, frames),
    # up run
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 160, 32, 32), 6, 1, True, frames),
    # left run
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 128, 32, 32), 6, 1, True, frames).flip_images(),
    # attack down
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 192, 32, 32), 4, 1, True, frames),
    # attack right
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 224, 32, 32), 4, 1, True, frames),
    # attack up
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 256, 32, 32), 4, 1, True, frames),
    # attack left
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 224, 32, 32), 4, 1, True, frames).flip_images(),
    # crawl right
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, 1, True, frames),
    # crawl left
    SpriteStripAnim(os.path.join(path, "Player/Player.png"), (0, 288, 32, 32), 4, 1, True, frames).flip_images(),
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
