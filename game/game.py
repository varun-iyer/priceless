from tkinter.font import names
from typing import Type
import arcade
import random
import numpy as  np
from sprites import SparseGrass, Mountain, Player, City, Tree, Water, CityManager

PLAYER_MOVEMENT_SPEED = 6
class CollectResourceView(arcade.View):
    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Click to Collect!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameView()
        self.window.show_view(game_view)

class Priceless(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        self.scene = None
        self.player_sprite = None
        self.city_sprite = None

        # Sprite lists
        self.tile_size = 16

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)


    def make_resource(self, x, y):
        return (np.cos(y) * np.tan(x) * np.cos(x)* np.tan(y)) > 0

    def get_random_resource(self):
        choices = {
            0: Tree,
            1: Mountain,
            2: Water
        }
        choice = random.randint(0,2)
        return choices[choice]


    def gather_dropoff_resource(self):
        resource_collision = self.check_collisions("Resources")
        if not resource_collision:
            return
        sprite = resource_collision.pop()
        if isinstance(sprite, City):
            print(sprite.get_current_level())
            print(sprite.get_totals())
            print(sprite.get_city_value())
            self.player_sprite.drop_off(sprite)
        else:
            print(sprite.resource.name)
            print(sprite.resource.amount)
            self.player_sprite.gather(sprite)
            print(sprite.resource.amount)

           
    def check_collisions(self, resource):
        hit_list = arcade.check_for_collision_with_lists(
            self.player_sprite, [self.scene[resource], self.scene["City"]]
        )
        return hit_list 


    def setup(self):
        """ Set up the game and initialize the variables. """

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Resources", use_spatial_hash=True)
        self.scene.add_sprite_list("Grass")
        self.scene.add_sprite_list("City", use_spatial_hash=True)

        self.player_sprite = Player()
        self.city_manager = CityManager()

        for x in range(0, self.width-16, 16):
            for y in range(0, self.height-16, 16):
                # choose tile from enum
                if (x == self.width//2) and (y == self.height//2):
                    scene_name = "Player"
                    tile = self.player_sprite
                elif (((x == self.width//2 + 16) or (x == self.width//2 - 16)) and
                      ((y == self.height//2 + 16) or (y == self.height//2 - 16))):
                      scene_name = "City"
                      tile = City(self.city_manager)
                elif self.make_resource(x/16, y/16): #tests
                    scene_name = "Resources"
                    tile = self.get_random_resource()()
                else:
                    scene_name = "Grass"
                    tile = SparseGrass()

                tile.center_x = x
                tile.center_y = y
                self.scene.add_sprite(scene_name, tile)
    
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.ENTER:
            self.gather_dropoff_resource() 

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.scene.update(names=["Player"])
        


def main():
    """ Main function """
    window = Priceless(800, 800, "Priceless")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
