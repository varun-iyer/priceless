from tkinter.font import names
from typing import Type
import arcade
import arcade.gui
import random
import os
import numpy as  np
from sprites import SparseGrass, Mountain, Player, City, Tree, Water, CityManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
PLAYER_MOVEMENT_SPEED = 6

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Priceless", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to learn how to play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)

class InstructionView(arcade.View):
    # to test if a text label can show up
    # def __init__(self):
    #     super().__init__()
    #     # Create a vertical BoxGroup to align buttons
    #     self.v_box = arcade.gui.UIBoxLayout()
    #     # Create a text label
    #     ui_text_label = arcade.gui.UITextArea(text="This is a Text Widget",
    #                                           width=450,
    #                                           height=40,
    #                                           font_size=24,
    #                                           font_name="Kenney Future")

    #     self.v_box.add(ui_text_label.with_space_around(top=0))
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("How to Play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.05 - 75,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Collect resources to expand your city and level up", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.25 - 75, 
                        arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Use the arrow keys to move across the board", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.35 - 75, 
                        arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press Enter on a tile that has a resource to acquire it", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.45 - 75, 
                        arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Reach level 10 to beat the game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.60 - 75, 
                        arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Priceless()
        game_view.setup()
        self.window.show_view(game_view)

class Priceless(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        self.scene = None
        self.player_sprite = None
        self.city_sprite = None

        # Sprite lists
        self.tile_size = 16

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # # Create a text label
        # ui_text_label = arcade.gui.UITextArea(text="This is a Text Widget",
        #                                       width=450,
        #                                       height=40,
        #                                       font_size=24,
        #                                       font_name="Kenney Future")


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

        for x in range(0, SCREEN_WIDTH-16, 16):
            for y in range(0, SCREEN_HEIGHT-16, 16):
                # choose tile from enum
                if (x == SCREEN_WIDTH//2) and (y == SCREEN_HEIGHT//2):
                    scene_name = "Player"
                    tile = self.player_sprite
                elif (((x == SCREEN_WIDTH//2 + 16) or (x == SCREEN_WIDTH//2 - 16)) and
                      ((y == SCREEN_HEIGHT//2 + 16) or (y == SCREEN_HEIGHT//2 - 16))):
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

        arcade.draw_text("Resources", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

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

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    

if __name__ == "__main__":
    main()
