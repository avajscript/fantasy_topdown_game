import copy
import json
import string

from pygame import Surface, image, sprite
import os
import constants
from abc import ABC, abstractmethod


class InteractableObject(ABC):
    @abstractmethod
    def redraw_images(self):
        pass

    @abstractmethod
    def draw(self, screen: Surface):
        pass


class Chest(InteractableObject, sprite.Sprite):
    def __init__(self, items: string, chest_image: Surface, x: int, y: int):
        super(Chest, self).__init__()
        self.items = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        for i, item in enumerate(json.loads(items)):
            self.items[i % 4][int(i / 4)] = item

        self.image = chest_image
        self.inventory_image = chest_image
        self.rect = self.image.get_rect(topleft=(x * constants.TILE_WIDTH, y * constants.TILE_WIDTH))

        self.x = x
        self.y = y

    def redraw_images(self):
        """
        Draws all the item images onto the main chest background image
        :return:
        """
        # Redraw the background image for the chest
        self.image = self.inventory_image.copy()
        # Iterate over each item to load the image and draw it on the correct location on the self.inventory_image
        for y, row in enumerate(self.items):
            for x, item in enumerate(row):
                if item is None:
                   continue
                img = constants.dyn_loaded_images.get(item["name"])
                # Load the image and add it to the loaded images dict if it doesn't exist in memory yet
                if img is None:
                    img = image.load(os.path.join(constants.image_file_path, item["image"]))
                    constants.dyn_loaded_images[item["name"]] = img
                # This will draw the loaded inventory image in the proper grid section.
                # Ex. 4x4 grid of items first will be 0,0, etc
                print("blitted sword")
                self.image.blit(img, (x * constants.TILE_WIDTH + constants.SPACING / 2, y / constants.INVENTORY_TILE_WIDTH + constants.SPACING / 2))

    def draw(self, screen: Surface):
        """
        Draws the chest onto the screen. If the chest items are updated, redraw_images() will need to be called
        :param screen: The screen to be drawn onto
        :return:
        """
        screen.blit(self.inventory_image, self.rect)

    def click_action(self, x: int, y: int):
        # Pixel coordinates of self.x and self.y
        x_px, y_px = self.x * constants.TILE_WIDTH, self.y * constants.TILE_WIDTH
        # Get x and y tile coordinates. Ex. 0, 1
        relative_x_coord = int((x - x_px) / constants.TILE_WIDTH)
        relative_y_coord = int((y - y_px) / constants.TILE_WIDTH)
        # fetch item from list based on x, y coords
        item = self.items[relative_x_coord][relative_y_coord]
        self.items[relative_x_coord][relative_y_coord] = None
        self.redraw_images()
        return item

    def print_items(self):
        for row in self.items:
            for item in row:
                print(f"item: {item}")
