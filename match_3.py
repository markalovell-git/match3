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
        self.grid.fill({
            "color" : 0,
            "type"  : "No Gem",
            "is matched" : False
        })

        self.number_list = [] # random list of numbers that feed into the number grid

    def print_out_number_grid(self):
        print ("*" * 80)
        for i in range(ROWS): # display bottom row first, easier for thinking in xy coords
            # print("Row {}: ".format(i))
            print_row = ""
            for j in range(COLS):  
                # print_row += str(self.grid[i][j]) 
                print_row += str(self.grid[i][j].get("color")) + "  "
            print(print_row + "\n")
        print ("*" * 80)

    def generate_new_number_list(self):
        random_number_list = []
        total_number_of_items_in_number_grid = np.count_nonzero(self.grid)
        for i in range(total_number_of_items_in_number_grid):
            random_number =  random.randint(1, NUM_OF_GEMS)
            random_number_list.append(random_number)
            # print(random_number_list)
        return(random_number_list)
            
    def check_grid_for_matches(self):
        for i in range(2, ROWS):
            for j in range(2, COLS):
                # horizontal check
                this_number = self.grid[i][j].get("color")
                one_to_the_left = self.grid[i][j-1].get("color")
                two_to_the_left = self.grid[i][j-2].get("color")
                one_above = self.grid[i-1][j].get("color")
                two_above = self.grid[i-2][j].get("color")

                # reverse the order of rows so that top row becomes bottom row  
                # making it easier to think in terms of x, y instead of x, -y 
                display_i = abs(i - ROWS) - 1
                if this_number == one_to_the_left == two_to_the_left:
                    print("Horizontal Match at {}, {}.".format(j, display_i))
                if this_number == one_above == two_above:
                    print("Vertical Match at {}, {}.".format(j,display_i))

    def populate_grid_with (self, number_list):
        for i in range(ROWS):
            for j in range(COLS): 
                this_number = number_list.pop(0)
                data = {
                    "color" : this_number,
                    "type"  : "3 Gem",
                    "is matched" : False
                }   
                self.grid[i][j] = data

number_grid = NumberGrid()
random_number_list = number_grid.generate_new_number_list()
number_grid.populate_grid_with(random_number_list)

number_grid.print_out_number_grid()   

number_grid.check_grid_for_matches()

# def main():
#     """ Main method """
#     window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#     window.setup()
#     arcade.run()
# if __name__ == "__main__":
#     main()