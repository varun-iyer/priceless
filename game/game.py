from tkinter.font import names
import arcade
import random
import numpy as  np
from sprites import SparseGrass, Mountain, Player, City, Tree, Water

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
        collision = resource_collision.pop()
        if isinstance(collision, City):
            print(collision.current_level)
            print(collision.totals)
            self.player_sprite.drop_off(collision)
        else:
            print(collision.resource.name)
            print(collision.resource.amount)
            self.player_sprite.gather(collision)
     
        print(collision.resource.amount)

           
    
    def check_collisions(self, resource):
        hit_list = arcade.check_for_collision_with_lists(
            self.player_sprite, [self.scene[resource]]
        )
        return hit_list 


    def setup(self):
        """ Set up the game and initialize the variables. """

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Resources", use_spatial_hash=True)
        self.scene.add_sprite_list("Grass")
        self.scene.add_sprite_list("City", use_spatial_hash=True)

        self.player_sprite = Player()
        self.city_sprite = City()

        for x in range(0, self.width-16, 16):
            for y in range(0, self.height-16, 16):
                # choose tile from enum
                if (x == self.width//2) and (y == self.height//2):
                    scene_name = "Player"
                    tile = self.player_sprite
                elif ((x == self.width//2 + 2) or (x == self.width//2 - 2) and
                      (y == self.height//2 + 2) or (y == self.height//2 - 2)):
                      scene_name = "City"
                      tile = self.city_sprite
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
