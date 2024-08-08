import json

from classes.Tile import Tile


class TileUtility():
    @staticmethod
    def remove_item(tile: Tile, item):
        json_items_prop = json.loads(tile.properties['items'])
        json_items_prop = [item_prop for item_prop in json_items_prop if item_prop['name'] != item['name']]
        tile.properties['items'] = json.dumps(json_items_prop)
