
import random
import numpy as np

from vars import ( COLS, ROWS, NUM_OF_GEMS)

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
        match = False
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
                    match = True
                if this_number == one_above == two_above:
                    print("Vertical Match at {}, {}.".format(j,display_i))
                    match = True
        return (match)

    def populate_grid_with (self, number_list):
        copy_number_list = number_list[:]
        for i in range(ROWS):
            for j in range(COLS): 
                random_index = random.randint(0, len(copy_number_list)-1)
                this_number = copy_number_list.pop(random_index)
                data = {
                    "color" : this_number,
                    "type"  : "3 Gem",
                    "is matched" : False
                }   
                self.grid[i][j] = data

    def init_number_grid(self):
        # print(number_grid)
        random_number_list = self.generate_new_number_list()
        # we want a starting grid with no matches
        grid_contains_match = True
        count = 0
        while grid_contains_match:
            count += 1
            print ("Grid populate attempt #{}".format(count))
            self.populate_grid_with(random_number_list)
            grid_contains_match = self.check_grid_for_matches()