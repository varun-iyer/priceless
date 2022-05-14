import arcade

class SparseGrass(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/tiles.png", 4, image_y=16*8, image_x=0, image_width=16, image_height=16)
