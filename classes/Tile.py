from pygame import sprite


class Tile(sprite.Sprite):
    def __init__(self, pos, surf, groups, properties, coords):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.properties = properties
        self.coords = coords

