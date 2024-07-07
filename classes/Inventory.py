import copy
import pygame as pg
from enum import Enum
import constants

class Item(pg.sprite.Sprite):
    def __init__(self, img: pg.Surface, properties, pos: tuple):
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.properties = properties

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

class InventoryDrawing(Enum):
    FULL_INVENTORY = 1
    ROW_AND_SLOT = 2

class Inventory(pg.sprite.Sprite):
    def __init__(self, inventory_img, inventory_row_img, inventory_slot_img):
        super(Inventory, self).__init__()
        self.items = []
        self.equipped_main_item = None
        self.equipped_secondary_items = []
        self.unequipped_items = []
        self.inventory_img: pg.Surface = inventory_img
        self.inventory_rect: pg.Rect = self.inventory_img.get_rect(topleft=(constants.SCREEN_WIDTH - self.inventory_img.get_width() - constants.BORDER_WIDTH, constants.BORDER_WIDTH))

        self.inventory_row_img: pg.Surface = inventory_row_img
        self.inventory_row_rect: pg.Rect = self.inventory_row_img.get_rect(topleft=(self.inventory_rect.topleft[0] - self.inventory_row_img.get_width() - constants.SPACING, self.inventory_rect.topleft[1]))

        self.inventory_slot_img: pg.Surface = inventory_slot_img
        self.inventory_slot_rect = self.inventory_slot_img.get_rect(topleft = (self.inventory_row_rect.topleft[0] - self.inventory_slot_img.get_width() - constants.SPACING, self.inventory_row_rect.topleft[1]))

    # Conditionally draw the inventory based on draw state
    def draw(self, screen: pg.Surface, draw_state: InventoryDrawing):
        if InventoryDrawing.FULL_INVENTORY:
            screen.blit(self.inventory_img, self.inventory_rect)
            screen.blit(self.inventory_row_img, self.inventory_row_rect)
            screen.blit(self.inventory_slot_img, self.inventory_slot_rect)

        elif InventoryDrawing.ROW_AND_SLOT:
            pass

    def loot_item(self, item):
        # Add to main slot if it's empty
        if self.equipped_main_item == None:
            self.equipped_main_item = item
        elif len(self.equipped_secondary_items) < constants.MAX_SECONDARY_INV_SPACES:
            self.equipped_secondary_items.append(item)
        else:
            self.unequipped_items.append(item)

        # Always add looted item to the main inventory
        self.items.append(item)

    # Remove and return

    def de_equip_item(self) -> Item:
        """
        Set the equipped item to None and return the equipped item
        :return: current equipped item
        """
        unequiped_item: Item = None
        if self.equipped_main_item != None:
            unequiped_item = copy.deepcopy(self.equipped_main_item)
            self.equipped_main_item = None
        return unequiped_item

    def equip_item(self, item: Item) -> Item:
        """
        Equip the item passed and return the currently equipped one
        :param item: The item to be equipped
        :return: The equipped item before the new item was equipped
        """
        currently_equipped_item = copy.deepcopy(self.equipped_main_item)
        self.equipped_main_item = item
        return currently_equipped_item

    def equip_from_secondary(self, index: int):
        # Get the item to equip from secondary items
        item_to_equip = self.equipped_secondary_items[index]
        self.equipped_secondary_items.remove(item_to_equip)

        # Set main item to secondary item and add main equipped item to secondary items
        self.equipped_secondary_items.insert(index, self.equipped_main_item)
        self.equipped_main_item = item_to_equip

    def equip_from_unequipped(self, index: int):
        # Get the item to equip from secondary items
        item_to_equip = self.unequipped_items[index]
        self.unequipped_items.remove(item_to_equip)

        # Set main item to secondary item and add main equipped item to secondary items
        self.unequipped_items.insert(index, self.equipped_main_item)
        self.equipped_main_item = item_to_equip

