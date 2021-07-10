import arcade
import math
import random
import platform
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Match Three!"
NUM_OF_GEMS = 6 # can't be greater than 7 unless I make new graphics

COLS = 3
ROWS = 5

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

class NumberGrid:
    """
    The mathematical numbergrid that underlies the display
    """

    def __init__(self, number_list):
        """
        Initializer
        """
        self.number_list = number_list
    
        new_number_list = []    
        for i in self.number_list:
            new_number_list.append(i*3)

        self.number_list = new_number_list

    def pokey(self):
        print("Pokey!")

    # def init_number_grid():
    #     # ng = np.empty_like(shape( object, dtype=object)
    #     ng = np.empty((ROWS, COLS), dtype=object)
    #     ng.fill([0, "No Gem"])

    #     return ng

    # def output_number_grid(ng):
    #     for i in range(ROWS):
    #         print("Row {}: ".format(i))
    #         print_row = ""
    #         for j in range(COLS):  
    #             print_row += str(ng[i][j])
    #         print(print_row + "\n")
    
    # number_grid = init_number_grid()

    # # populate()
    # number_grid[4][2] = [1, "3gem"]

    # output_number_grid(number_grid)

number_list = [1, 2, 3, 4, 5]
number_grid = NumberGrid(number_list)
print(vars(number_grid))
# print(number_grid[3][2])
number_grid.pokey()   

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == "__main__":
    main()