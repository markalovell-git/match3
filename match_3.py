import arcade
import math
import random
import platform
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Match Three!"

class MyGame(arcade.Window):
    """
    Main application class.
    """
    # mouse_press_x = 0
    # mouse_press_y = 0
    # mouse_release_x = 0
    # mouse_release_y = 0

    # drop_jitter = .90
    # drop_height = SCREEN_HEIGHT

    # gem_to_move = Gem
    # gem_being_moved = Gem
    # destroy_gem_index = 0
    
    # game_state = "booting"
    # switch_free_range_mode = False
    
    # PAUSE = False

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.gem_list = None
        self.special_gem_list = None
        self.foreground_gem_list = None
        self.icons_list = None

        # Declare Variables
        self.gem_sprite = None
        self.number_grid = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # # Don't show the mouse cursor
        # self.set_mouse_visible(False)
    def setup(self):
        """ Set up the game and initialize the variables. """

        self.drop_jitter = .90
        self.drop_height = SCREEN_HEIGHT

        self.game_state = "initializing"
        self.game_state_temp = ""
        self.switch_free_range_mode = False

        self.wait_timer = 0
        self.moves_remain_list = []
    
        # Sprite lists
        self.gem_list = arcade.SpriteList()
        self.special_gem_list = arcade.SpriteList()
        self.foreground_gem_list = arcade.SpriteList()
        self.icons_list = arcade.SpriteList()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()