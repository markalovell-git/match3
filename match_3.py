import arcade
import math
import random
import platform
import numpy as np
from numbergrid import NumberGrid


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None
        # self.gem_list = None

        # Declare Variables
        # self.gem_sprite = None


        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # # Don't show the mouse cursor
        # self.set_mouse_visible(False)
        
    def setup(self):
        """ Set up the game and initialize the variables. """
    
        # Sprite lists
        self.gem_list = arcade.SpriteList()


class Gem:
    """
    The basic Gem building block of the game
    """


number_grid = NumberGrid()
number_grid.init_number_grid()
number_grid.print_out_number_grid()



# def main():
#     """ Main method """
#     window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#     window.setup()
#     arcade.run()
# if __name__ == "__main__":
#     main()