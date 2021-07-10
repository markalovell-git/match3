import arcade
import math
import random
import platform
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Match Three!"
NUM_OF_GEMS = 6 # can't be greater than 7 unless I make new graphics

COLS = 5
ROWS = 8

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


    def __init__(self):
        """
        Initializer
        """

        self.grid = np.empty((ROWS, COLS), dtype=object)
        self.grid.fill([0, "No Gem"])
        self.number_list = [] # random list of numbers that feed into the number grid

    def print_out_number_grid(self):
        print ("*" * 80)
        for i in range(ROWS):
            # print("Row {}: ".format(i))
            print_row = ""
            for j in range(COLS):  
                # print_row += str(self.grid[i][j]) 
                print_row += (str(self.grid[i][j][0]) + "  ")  
            print(print_row + "\n")
        print ("*" * 80)

    def generate_new_number_list(self):
        total_number_of_items_in_number_grid = np.count_nonzero(self.grid)
        for i in range(total_number_of_items_in_number_grid):
            random_number =  random.randint(1, NUM_OF_GEMS)
            self.number_list.append(random_number)
            
    def grid_has_matches(self):
        for i in range(ROWS):
            for j in range(COLS):
                # horizontal check
                try:
                    this_number = self.grid[i][j][0]
                    one_to_the_left = self.grid[i][j-1][0]
                    two_to_the_left = self.grid[i][j-2][0]
                except:
                    pass
                # vertical check
    def populate_grid_with (self, number_list):
        for i in range(ROWS):
            for j in range(COLS): 
                this_number = number_list.pop(0)
                data = [this_number, "3Gem"]
                self.grid[i][j] = data

    def change_number_grid_xy(self, row, col, arg):
        grid = self.grid
        grid[col-1,row-1] = [2, "gem"]

    # number_grid = init_number_grid()

    # # populate()
    # number_grid[4][2] = [1, "3gem"]

    # output_number_grid(number_grid)

number_grid = NumberGrid()
number_grid.generate_new_number_list()

# print(number_grid.number_list)
number_grid.populate_grid_with(number_grid.number_list)

number_grid.print_out_number_grid()   

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
if __name__ == "__main__":
    main()