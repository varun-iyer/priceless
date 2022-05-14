import arcade
import random
from sprites import SparseGrass

class Priceless(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Sprite lists
        self.tile_list = None
        self.figure_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.tile_list = arcade.SpriteList()
        self.figure_list = arcade.SpriteList()

        # should use itertools but w/e
        for x in range(0, 16 * 16, 16):
            for y in range(0, 16 * 16, 16):
                # choose tile from enum
                tile = SparseGrass()
                tile.center_x = x
                tile.center_y = y
                print(x, y)
                self.tile_list.append(tile)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.tile_list.draw()
        self.figure_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        pass


def main():
    """ Main function """
    window = Priceless(16 * 16, 16 * 16, "Priceless")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
