#!/usr/bin/env python3

# At the unix command prompt, type the following to make myscript.py executable: 
# $ chmod +x myscript.py. 
# ove myscript.py into your bin directory, and it will be runnable from anywhere.
# Source: https://ostoday.org/linux/how-to-update-python-on-linux.html

import arcade
import math
import random
import platform
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Match Three!"

ROWS = 8
COLUMNS = 5
GEM_SPEED = 10 #20
ACCELERATION = 1.06 #1.08
FLOOR_POSITION = 100
ANIM_UPDATES_PER_FRAME = 10
NUM_OF_GEMS = 6 # can't be greater than 7 unless I make new graphics

PAUSE = False

def trans_cr_to_xy(c, r):
    trans_c = ((c * 68) + ((SCREEN_WIDTH / 2) - ((COLUMNS - 1) * 34))) 
    this_r = abs(r - (ROWS -1))
    trans_r = ((this_r * 68) + FLOOR_POSITION)
    return trans_c, trans_r

def trans_xy_to_cr(x, y):
    trans_x = int((x - (SCREEN_WIDTH / 2) + ((COLUMNS - 1) * 34)) / 68)
    this_y = int((y - FLOOR_POSITION) / 68)
    trans_y = abs(this_y - (ROWS - 1))
    return trans_x, trans_y

def get_dist_between_points(p1, p2):
        #p1 = self.gem_to_move.start_pos
        #p2 = self.gem_to_move.end_pos

        distance = int(math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)) )
        return(distance)

def move_towards_point(this_sprite, to_pos):

    # print(from_pos, to_pos)
    # print(from_pos[0], from_pos[1])
    #myradians = math.atan2(to_y - this_sprite.center_y, to_x - this_sprite.center_x)
    # myradians = math.atan2(to_pos[1] - from_pos[1], to_pos[0] - from_pos[0])
    myradians = math.atan2(to_pos[1] - this_sprite.center_y, to_pos[0] - this_sprite.center_x)

    # need to subtract 90 degrees due to weirdness
    mydegrees = int(math.degrees(myradians))
    mydegrees -= 90
    myradians = math.radians(mydegrees)

    # Use math to find our change based on our speed and angle
    this_sprite.center_x += -this_sprite.speed * math.sin(myradians)
    this_sprite.center_y += this_sprite.speed * math.cos(myradians)

    current_distance = (get_dist_between_points([this_sprite.center_x, this_sprite.center_y], to_pos))
    # print(current_distance)
    # current_dist_percentage = ((current_distance/total_distance)*100)
    # print(str(int(current_dist_percentage)) + "%")
    
    # lerp(this_sprite, current_dist_percentage)

    this_sprite.speed *= ACCELERATION 

    if this_sprite.speed > 50:
        this_sprite.speed = 30

    if current_distance <= this_sprite.speed:
        this_sprite.center_x = to_pos[0]
        this_sprite.center_y = to_pos[1]
        # print (f"this sprite state = {this_sprite.state}")
        this_sprite.speed = 0

        # print("Done moving sprite!")
        # this_sprite.remove_from_sprite_lists()


class Gem(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create various variables 
        self.speed = 0
        self.index = 0
        self.inspect_matches = True
        self.is_matched = False
        self.category = None
        self.column = 0
        self.row = 0
        self.timer = 0

        # 5 GEM Used for flipping between image sequences
        self.texture_index = random.randint((1+8), (6+8) * ANIM_UPDATES_PER_FRAME - 9)

        # 5 GEM textures for flashing
        self.flash_textures = []
        for i in range(1,8):
            if platform.system() == "Windows":
                texture2 = arcade.load_texture(f"static//pngs//Gems_03_64x64_00{i}.png")
            else:
                texture2 = arcade.load_texture(f"static/pngs/Gems_03_64x64_00{i}.png")
            self.flash_textures.append(texture2)

    
    def update(self):

        if self.category == "moving to be destroyed":
            move_to_x, move_to_y = 100, 100 # trans_cr_to_xy(self.column, self.row)
            move_towards_point(self, [move_to_x, move_to_y])
            if self.speed == 0:
                self.kill()

        elif self.category == "5Gem":
            self.scale -= 0.02
            if self.scale < 1:
                self.scale = 1

    def update_animation(self,delta_time: float = 1/60):

        if self.category == "5Gem":
            # flashing animation
            self.texture_index += 1
            # print(self.texture_index)
            if self.texture_index > (6 * ANIM_UPDATES_PER_FRAME - 1) :
                self.texture_index = 0 
            frame = self.texture_index // ANIM_UPDATES_PER_FRAME
            self.texture = self.flash_textures[frame]
        
        elif self.category == "4Gem":
            i = self.index
            if platform.system() == "Windows":
                self.append_texture(arcade.load_texture(f"static//pngs//Gems_02_64x64_00{i}.png"))
            else:
                self.append_texture(arcade.load_texture(f"static/pngs/Gems_02_64x64_00{i}.png"))
            self.set_texture(1)

        elif self.category == "CrossGem":
            i = self.index
            if platform.system() == "Windows":
                self.append_texture(arcade.load_texture(f"static//pngs//Gems_03_64x64_00{i}.png"))
            else:
                self.append_texture(arcade.load_texture(f"static/pngs/Gems_03_64x64_00{i}.png"))
            self.set_texture(1)

class MyGame(arcade.Window):
    """
    Main application class.
    """
    mouse_press_x = 0
    mouse_press_y = 0
    mouse_release_x = 0
    mouse_release_y = 0

    drop_jitter = .90
    drop_height = SCREEN_HEIGHT

    gem_to_move = Gem
    gem_being_moved = Gem
    destroy_gem_index = 0
    
    game_state = "booting"
    switch_free_range_mode = False
    
    PAUSE = False

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

        # Don't show the mouse cursor
        self.set_mouse_visible(False)


    # check to see if gems are idle or not
    def are_gems_moving(self):
                gems_moving = False
                for gem in self.gem_list:   
                    if gem.speed != 0:
                        gems_moving = True
                        break
                for gem in self.special_gem_list:   
                    if gem.speed != 0:
                        gems_moving = True
                        break
                for gem in self.foreground_gem_list:   
                    if gem.speed != 0:
                        gems_moving = True
                        break
                return(gems_moving)


    def create_gem(self, r, c):

        if self.number_grid[r, c] == 0:  # choose a random index to fill in missing gems from top row
            i = random.randint(1, NUM_OF_GEMS)
            self.number_grid[r, c] = i
        elif self.number_grid[r, c] == 99: # this is a flashing 5Gem
            i = 1
        else: # choose an index based on the tested number_grid for the initial layout
            i = int(self.number_grid[r][c])

        gem = self.gem_sprite
        if platform.system() == "Windows":
            gem = eval("Gem('static//pngs//Gems_01_64x64_00" + str(i) + ".png', 1)")
        else:
            self.gem_sprite = eval("Gem('static/pngs/Gems_01_64x64_00" + str(i) + ".png', 1)")

        gem.column = c
        gem.row = r
        this_x, this_y = trans_cr_to_xy(c, r)
        gem.center_x = this_x
        gem.center_y = this_y + self.drop_height
        gem.speed = GEM_SPEED
        gem.state = "waiting to fall"
        self.gem_list.append(gem)
        self.inspect_matches = True

        if self.number_grid[r, c] == 99:
            gem.index = 99
            gem.category = "5Gem"
        else: 
            gem.index = i


    def add_columns(self, ng, this_gem_list):
        # add 1 column of zeroes on either side of the current number_grid
        # this increases the number_grid by 2 columns
        # print(f"adding {num} columns")

        this_columns = len(ng[1])
        print (this_columns)
        ng = (np.insert(ng, 0, 0, axis = 1))
        ng = (np.insert(ng, this_columns + 1, 0, axis = 1))
        for gem in this_gem_list:
            gem.column += 1

        this_columns += 2

        return (ng, this_columns)


    def are_matches_in_number_grid(self, ng):
        check = False
        for i in range (ROWS):
            for j in range (COLUMNS):
                if i > 1:
                    if ng[i][j] == ng[i-1][j] and ng[i][j] == ng[i-2][j]:
                        # print ("Horizontal Match Found. Start Over.")
                        check = True
                if j > 1:
                    if ng[i][j] == ng[i][j-1] and ng[i][j] == ng[i][j-2]:
                        # print("Vertical Match Found. Start Over.")
                        check = True
        return check


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

        def generate_number_grid():
            ng = np.zeros((ROWS, COLUMNS))
            for i in range(COLUMNS):
                for j in range(ROWS):              
                    ng[j][i] = random.randint(1, NUM_OF_GEMS)
            return(ng)

            # print("No Matches Found. Success!")
            return True

        def print_number_grid():
            # Set up the gems
            for c in range(COLUMNS):
                for r in range(ROWS):
                    self.create_gem(r, c)
                    
        def set_up_mouse_pointer_sprite():
            if platform.system() == "Windows":
                self.mouse_pointer_sprite = arcade.Sprite("static\\pngs\\glove3.png", 1)
            else:
                self.mouse_pointer_sprite = arcade.Sprite("static/pngs/glove3.png", 1)
            self.mouse_pointer_sprite.center_x = -100
            self.mouse_pointer_sprite.center_y = -100
            self.mouse_pointer_sprite.alpha = 255
            self.icons_list.append(self.mouse_pointer_sprite)

            if platform.system() == "Windows":
                self.mouse_pointer_active_sprite = arcade.Sprite("static\\pngs\\slick_arrow-delta.png", 1)
            else: 
                self.mouse_pointer_active_sprite = arcade.Sprite("static/pngs/slick_arrow-delta.png", 1)
            self.mouse_pointer_active_sprite.center_x = -100
            self.mouse_pointer_active_sprite.center_y = -100
            self.mouse_pointer_active_sprite.alpha = 0
            self.icons_list.append(self.mouse_pointer_active_sprite)

        valid_grid = False
        while valid_grid == False:
            this_number_grid = generate_number_grid()
            valid_grid = not self.are_matches_in_number_grid(this_number_grid)
        else:
            self.number_grid = this_number_grid

        # ______________________________________________________________
        # TODO: REMOVE THIS. TESTING PURPOSES ONLY
        self.number_grid[0] = [2,4,1,1,3]
        self.number_grid[1] = [5,5,1,5,4]
        self.number_grid[2] = [1,1,5,1,1]
        self.number_grid[3] = [2,4,1,1,3]
        self.number_grid[4] = [5,5,1,5,99]
        # # self.number_grid[5] = [4,2,99,3,1]
        # # self.number_grid[6] = [99,99,2,99,99]
        # ______________________________________________________________
        
        print_number_grid()
        set_up_mouse_pointer_sprite()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the Sprites.
        try:
            self.gem_list.draw()
            if self.special_gem_list:
                self.special_gem_list.draw()
            if self.foreground_gem_list:
                self.foreground_gem_list.draw()
            self.icons_list.draw()
        except: 
            pass

        # Draw Text
        arcade.draw_text(self.game_state, 50, 410, arcade.color.WHITE, 15)

        # display mouse coordinates
        mouse_x = self.mouse_pointer_sprite.center_x
        mouse_y = self.mouse_pointer_sprite.center_y
        arcade.draw_text(f"mouse x, y: {str(mouse_x)} {str(mouse_y)}", 50, 430, arcade.color.WHITE, 12)

        # display self.are_gems_moving()
        arcade.draw_text(f"Are gems moving? {self.are_gems_moving()}", 50, 450, arcade.color.WHITE, 15)

        # display if gems are selected
        if self.gem_to_move:
            arcade.draw_text(f"Gem 1 selected!", 50, 350, arcade.color.YELLOW, 16)
        if self.gem_being_moved:
            arcade.draw_text(f"Gem 2 selected!", 50, 330, arcade.color.YELLOW, 16)

        # display gem mouse-over
        gem_hit_list = arcade.check_for_collision_with_list(self.mouse_pointer_active_sprite, self.gem_list)
        for gem in gem_hit_list:
            arcade.draw_text(f"Gem index {gem.index} at: {gem.column}, {gem.row}", 50, 620, arcade.color.WHITE, 12)
            arcade.draw_text(f"Grid index {self.number_grid[gem.row, gem.column]}", 50, 600, arcade.color.WHITE, 12)
            arcade.draw_text(f"Gem State '{gem.state}'", 50, 580, arcade.color.WHITE, 12)
            arcade.draw_text(f"Inspect Gem for Matches: '{gem.inspect_matches}'", 50, 560, arcade.color.WHITE, 12)
            arcade.draw_text(f"is matched?  {gem.is_matched}", 50, 540, arcade.color.WHITE, 12)
            arcade.draw_text(f"Speed: {gem.speed}", 50, 520, arcade.color.WHITE, 12)
            arcade.draw_text(f"Category: {gem.category}", 50, 500, arcade.color.WHITE, 12)
            arcade.draw_text(f"Layer: gem_list", 50, 480, arcade.color.WHITE, 12) 
            

        gem_hit_list = arcade.check_for_collision_with_list(self.mouse_pointer_active_sprite, self.foreground_gem_list)
        for gem in gem_hit_list:
            arcade.draw_text(f"Gem index {gem.index} at: {gem.column}, {gem.row}", 50, 620, arcade.color.WHITE, 12)
            arcade.draw_text(f"Grid index {self.number_grid[gem.row, gem.column]}", 50, 600, arcade.color.WHITE, 12)
            arcade.draw_text(f"Gem State '{gem.state}'", 50, 580, arcade.color.WHITE, 12)
            arcade.draw_text(f"Inspect gem for matches: '{gem.inspect_matches}'", 50, 560, arcade.color.WHITE, 12)
            arcade.draw_text(f"is matched?  {gem.is_matched}", 50, 540, arcade.color.WHITE, 12)
            arcade.draw_text(f"Speed: {gem.speed}", 50, 520, arcade.color.WHITE, 12)
            arcade.draw_text(f"Category: {gem.category}", 50, 500, arcade.color.WHITE, 12)
            arcade.draw_text(f"Layer: foreground", 50, 480, arcade.color.WHITE, 12) 
    
        if self.switch_free_range_mode == True:
            arcade.draw_text("Free Switch Mode Active", 50, 300, arcade.color.ORANGE, 15)
        
        if self.PAUSE == True:
            arcade.draw_text("PAUSED", 50, 250, arcade.color.WHITE, 30)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # get the gem object from the number_grid at row, column
        def gem_at(row, column):
            this_x, this_y = trans_cr_to_xy(column, row)
            # print(this_x, this_y)
            gem_at_this_row_and_column = Gem
            for gem in self.gem_list:
                if gem.collides_with_point(tuple([this_x, this_y])):
                    gem_at_this_row_and_column = gem
            
            return gem_at_this_row_and_column

    
        def check_for_special_matches():

            def make_and_check_temp_gem_list(category, this_list):

                # make a temp list of all the gems to check   
                a_list = [x for x in this_list]

                # 5Gem special code
                if category == "5Gem_group":
                    for i in range(len(a_list)):
                        only_unmarked_gems_in_combo = True
                        if a_list[i].category != None:
                            only_unmarked_gems_in_combo = False
                            return
                    if only_unmarked_gems_in_combo:
                        # do stuff to 'follower gems'
                        for i in range(len(a_list)):
                            if a_list[i] != gem:
                                ng[a_list[i].row, a_list[i].column] = 0
                                a_list[i].row = gem.row
                                a_list[i].column = gem.column
                                a_list[i].category = "gem_follower"
                                a_list[i].is_matched = True
                            else: 
                                # do stuff to 'main gem'
                                gem.category = "proto_5Gem"
                                gem.inspect_matches = False
                                self.foreground_gem_list.append(gem)
                                self.gem_list.remove(gem)
                            # gem.index = 99 -- have to do this later in the program so it doesn't suddenly appear
                        return 
                
                # 4 Gem match special code
                if category == "4Gem_group":
                    for i in range(len(a_list)):
                        only_unmarked_gems_in_combo = True
                        if a_list[i].category != None:
                            only_unmarked_gems_in_combo = False
                            return
                    if only_unmarked_gems_in_combo:
                        for i in range(len(a_list)):
                            if a_list[i] != gem:
                                ng[a_list[i].row, a_list[i].column] = 0
                                a_list[i].row = gem.row
                                a_list[i].column = gem.column
                                a_list[i].category = "gem_follower"
                                a_list[i].is_matched = True
                            else:
                                # do stuff to 'main gem'
                                gem.category = "proto_4Gem"
                                gem.inspect_matches = False
                                self.foreground_gem_list.append(gem)
                                self.gem_list.remove(gem)

                # 5Gem special code - L shapes
                if category == "CrossGem_group":
                    # print("FIVE GEM MATCH!")
                    # do stuff to 'follower gems'
                    for i in range(len(a_list)):
                        only_unmarked_gems_in_combo = True
                        if a_list[i].category != None:
                            only_unmarked_gems_in_combo = False
                            return
                    if only_unmarked_gems_in_combo:
                        for i in range(len(a_list)):
                            if a_list[i] != gem:
                                ng[a_list[i].row, a_list[i].column] = 0
                                a_list[i].row = gem.row
                                a_list[i].column = gem.column
                                a_list[i].category = "gem_follower"
                                a_list[i].is_matched = True
                            else: 
                                # do stuff to 'main gem'
                                gem.category = "proto_CrossGem"
                                gem.inspect_matches = False
                                self.foreground_gem_list.append(gem)
                                self.gem_list.remove(gem)
                            # gem.index = 99 -- have to do this later in the program so it doesn't suddenly appear
                        return 


                                
                return

            def check_5Gem_straight():
                #############  FIVE  ##############
                # horizontal 5 - two to the left, two to the right (fivesome) 
                # make a list of the two-left and two-right gems to check

                left2_gem = (r, c - 2)
                left1_gem = (r, c - 1)
                right1_gem = (r, c + 1)
                right2_gem = (r, c + 2)

                up2_gem = (r - 2, c)
                up1_gem = (r - 1, c)
                down1_gem = (r + 1, c)
                down2_gem = (r + 2, c)

                temp_list = []
                if c > 1 and c < COLUMNS - 2:
                    if ng[left2_gem] == ng[left1_gem] == ng[r,c] == ng[right1_gem] == ng[right2_gem]:
                        temp_list = [gem_at(left2_gem[0], left2_gem[1]),
                                    gem_at(left1_gem[0], left1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(right1_gem[0], right1_gem[1]),
                                    gem_at(right2_gem[0], right2_gem[1])]

                        # if 2 up
                        if (r > 1) and (ng[up2_gem] == ng[up1_gem] == ng[r,c]):
                            temp_list.extend(( gem_at(up2_gem[0], up2_gem[1]),
                                            gem_at(up1_gem[0], up1_gem[1]) ))

                        # elif 2 down
                        elif (r < ROWS - 2) and (ng[down2_gem] == ng[down1_gem] == ng[r,c]):
                            temp_list.extend(( gem_at(down2_gem[0], down2_gem[1]),
                                            gem_at(down1_gem[0], down1_gem[1]) ))

                        make_and_check_temp_gem_list("5Gem_group", temp_list)
                        return

                # vertical 5 - 2 above and 2 below (fivesome) 
                # make a list of the two-up and two-down gems to check
                temp_list = []
                if r > 1 and r < ROWS - 2:
                    if (ng[up2_gem] == ng[up1_gem] == ng[r,c] == ng[down1_gem] == ng[down2_gem]): 
                        temp_list = [gem_at(up2_gem[0], up2_gem[1]),
                                    gem_at(up1_gem[0], up1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(down1_gem[0], down1_gem[1]),
                                    gem_at(down2_gem[0], down2_gem[1])]

                        # if 2 left
                        if (c > 1) and (ng[left2_gem] == ng[left1_gem] == ng[r,c]):
                            temp_list.extend(( gem_at(left2_gem[0], left2_gem[1]),
                                            gem_at(left1_gem[0], left1_gem[1]) ))

                        # elif 2 right
                        elif (c < COLUMNS - 2) and (ng[right2_gem] == ng[right1_gem] == ng[r,c]):
                            temp_list.extend(( gem_at(right2_gem[0], right2_gem[1]),
                                            gem_at(right1_gem[0], right1_gem[1]) ))

                        make_and_check_temp_gem_list("5Gem_group", temp_list)
                        return

            def check_4Gem():
                #############  FOUR  ##############
                # horizontal 4 - two to the left, one to the right (foursome)

                left2_gem = (r, c - 2)
                left1_gem = (r, c - 1)
                right1_gem = (r, c + 1)
                right2_gem = (r, c + 2)

                up2_gem = (r - 2, c)
                up1_gem = (r - 1, c)
                down1_gem = (r + 1, c)
                down2_gem = (r + 2, c)

                # horizontal 4 - two to the left, one to the right (foursome)
                temp_list = []
                if c > 1 and c < COLUMNS - 1:
                    if ng[left2_gem] == ng[left1_gem] == ng[r,c] == ng[right1_gem]:
                        temp_list = [gem_at(left2_gem[0], left2_gem[1]),
                                    gem_at(left1_gem[0], left1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(right1_gem[0], right1_gem[1])]

                        make_and_check_temp_gem_list("4Gem_group", temp_list)
                        return

                # horizontal 4 - one to the left, two to the right (foursome)
                temp_list = []
                if c > 0 and c < COLUMNS - 2:
                    if ng[left1_gem] == ng[r,c] == ng[right1_gem] == ng[right2_gem]:
                        temp_list = [gem_at(left1_gem[0], left1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(right1_gem[0], right1_gem[1]), 
                                    gem_at(right2_gem[0], right2_gem[1])]

                        make_and_check_temp_gem_list("4Gem_group", temp_list)
                        return

                # vertical 4 - 2 above and 1 below (foursome)
                temp_list = []
                if r > 1 and r < ROWS - 1:
                    if ng[up2_gem] == ng[up1_gem] == ng[r,c] == ng[down1_gem]:
                        temp_list = [gem_at(up2_gem[0], up2_gem[1]),
                                    gem_at(up1_gem[0], up1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(down1_gem[0], down1_gem[1])]

                        make_and_check_temp_gem_list("4Gem_group", temp_list)
                        return

                # vertical 4 - 1 above and 2 below (foursome)
                temp_list = []
                if r > 0 and r < ROWS - 2:
                    if (ng[up1_gem] == ng[r,c] == ng[down1_gem] == ng[down2_gem]):
                        temp_list = [gem_at(up1_gem[0], up1_gem[1]),
                                    gem_at(r,c),
                                    gem_at(down1_gem[0], down1_gem[1]),
                                    gem_at(down2_gem[0], down2_gem[1])]
                            
                        make_and_check_temp_gem_list("4Gem_group", temp_list)
                        return

            def check_Cross_Gem():
                #############  FIVE  ##############
                # okay now let's do the wierd L shaped 5gem forms: 12:15, 6:15, 6:45, 12:45

                left2_gem = (r, c - 2)
                left1_gem = (r, c - 1)
                right1_gem = (r, c + 1)
                right2_gem = (r, c + 2)

                up2_gem = (r - 2, c)
                up1_gem = (r - 1, c)
                down1_gem = (r + 1, c)
                down2_gem = (r + 2, c)

                # 12:15
                temp_list = []
                if r > 1 and c < COLUMNS - 2:
                    if ng[up2_gem] == ng[up1_gem] == ng[r,c] == ng[right1_gem] == ng[right2_gem]:
                        temp_list = [gem_at(up2_gem[0], up2_gem[1]),
                                    gem_at(up1_gem[0], up1_gem[1]),
                                    gem_at(r,c), 
                                    gem_at(right1_gem[0], right1_gem[1]), 
                                    gem_at(right2_gem[0], right2_gem[1])]

                        # if one below
                        if (r < ROWS - 1) and (ng[down1_gem] == ng[r,c]):
                            temp_list.append( gem_at(down1_gem[0], down1_gem[1]) )
                        # if one to the left
                        if (c > 0) and (ng[left1_gem] == ng[r,c]):
                            temp_list.append( gem_at(left1_gem[0], left1_gem[1]) )

                        make_and_check_temp_gem_list("CrossGem_group", temp_list)
                        return

                # 6:15
                temp_list = []
                if r < ROWS - 2 and c < COLUMNS - 2:
                    if ng[right2_gem] == ng[right1_gem] == ng[r,c] == ng[down1_gem] == ng[down2_gem]:
                        temp_list = [gem_at(right2_gem[0], right2_gem[1]),
                                    gem_at(right1_gem[0], right1_gem[1]), 
                                    gem_at(r,c),
                                    gem_at(down1_gem[0], down1_gem[1]),
                                    gem_at(down2_gem[0], down2_gem[1])]

                        # if one above
                        if (r > 0) and (ng[up1_gem] == ng[r,c]):
                            temp_list.append( gem_at(up1_gem[0], up1_gem[1]) )
                        # if one to the left
                        if (c > 0) and (ng[left1_gem] == ng[r,c]):
                            temp_list.append( gem_at(left1_gem[0], left1_gem[1]) )

                        make_and_check_temp_gem_list("CrossGem_group", temp_list)
                        return

                # 6:45
                temp_list = []
                if r < ROWS - 2 and c > 1:
                    if ng[left2_gem] == ng[left1_gem] == ng[r,c] == ng[down1_gem] == ng[down2_gem]:
                        temp_list = [gem_at(left2_gem[0], left2_gem[1]),
                                    gem_at(left1_gem[0], left1_gem[1]), 
                                    gem_at(r,c),
                                    gem_at(down1_gem[0], down1_gem[1]),
                                    gem_at(down2_gem[0], down2_gem[1])]

                        # if one above
                        if (r > 0) and (ng[up1_gem] == ng[r,c]):
                            temp_list.append( gem_at(up1_gem[0], up1_gem[1]) )
                        # if one to the right
                        if (c < COLUMNS - 1) and (ng[right1_gem] == ng[r,c]):
                            temp_list.append( gem_at(right1_gem[0], right1_gem[1]) )

                        make_and_check_temp_gem_list("CrossGem_group", temp_list)
                        return

                #12:45
                temp_list = []
                if r > 1 and c > 1:
                    if ng[left2_gem] == ng[left1_gem] == ng[r,c] == ng[up1_gem] == ng[up2_gem]:
                        temp_list = [gem_at(left2_gem[0], left2_gem[1]),
                                    gem_at(left1_gem[0], left1_gem[1]), 
                                    gem_at(r,c),
                                    gem_at(up1_gem[0], up1_gem[1]), 
                                    gem_at(up2_gem[0], up2_gem[1])]

                        # if one below
                        if (r < ROWS - 1) and (ng[down1_gem] == ng[r,c]):
                            temp_list.append( gem_at(down1_gem[0], down1_gem[1]) )
                        # if one to the right
                        if (c < COLUMNS - 1) and (ng[right1_gem] == ng[r,c]):
                            temp_list.append( gem_at(right1_gem[0], right1_gem[1]) )

                        make_and_check_temp_gem_list("CrossGem_group", temp_list)
                        return

            ### Begin Actual Code ###

            # check 5Gem straight line
            for gem in self.gem_list:
                if gem.inspect_matches == True:
                    
                    ng = self.number_grid
                    r = gem.row
                    c = gem.column

                    check_5Gem_straight()

            # check CrossGem
            for gem in self.gem_list:
                if gem.inspect_matches == True:
                    
                    ng = self.number_grid
                    r = gem.row
                    c = gem.column

                    check_Cross_Gem()

            # check 4Gem
            for gem in self.gem_list:
                if gem.inspect_matches == True:
                    
                    ng = self.number_grid
                    r = gem.row
                    c = gem.column

                    check_4Gem()




        def check_regular_matches():
                
                for gem in self.gem_list:

                    c= gem.column
                    r = gem.row
                    ng = self.number_grid

                    right1_gem = (r, c + 1)
                    right2_gem = (r, c + 2)

                    down1_gem = (r + 1, c)
                    down2_gem = (r + 2, c)


                    # if any of these hit a special gem, then do special gem stuff. 

                    # horizontal 3 - two to the left
                    temp_list = []
                    if c < COLUMNS - 2:
                        if ng[r,c] == ng[right1_gem] == ng[right2_gem]:
                            temp_list = [gem_at(r,c),
                                        gem_at(right1_gem[0], right1_gem[1]),
                                        gem_at(right2_gem[0], right2_gem[1])]

                            for check_gem in temp_list:
                                check_gem.is_matched = True

                    # vertical 3 - 2 below
                    temp_list = []
                    if r < ROWS - 2:
                        if ng[r,c] == ng[down1_gem] == ng[down2_gem]:
                            temp_list = [gem_at(r,c),
                                        gem_at(down1_gem[0], down1_gem[1]),
                                        gem_at(down2_gem[0], down2_gem[1])]

                            for check_gem in temp_list:
                                check_gem.is_matched = True

        
        def check_player_moves_available():
                    ng = self.number_grid

                    for r in range(ROWS):
                        for c in range(COLUMNS):
                            
                            moves_remain_list = []

                            # check to see if there are any 5Gems
                            if self.number_grid[r, c] == 99:
                                if r > 0:
                                    moves_remain_list = [gem_at(r, c), gem_at(r - 1, c)]
                                    return (moves_remain_list)
                                else:
                                    moves_remain_list = [gem_at(r, c), gem_at(r + 1, c)]
                                    return (moves_remain_list)

                            # check horizontal 
                            right1_gem = (r, c + 1)
                            right1_over_gem = (r, c + 3)
                            left1_over_gem = (r, c - 2)

                            diagUp_right_gem = (r - 1, c + 2)
                            diagDown_right_gem = (r + 1, c + 2)

                            diagUp_left_gem = (r - 1, c - 1)
                            diagDown_left_gem = (r + 1, c - 1)

                            right2_gem = (r, c + 2)
                            triangle_down_gem = (r + 1, c + 1)
                            triangle_up_gem = (r - 1, c + 1)

                            if c < COLUMNS - 1:
                                if ng[r,c] == ng[right1_gem]:
                                    # gem_at(r, c).center_y  += 10
                                    # gem_at(right1_gem[0],right1_gem[1]).center_y += 10
                                    
                                    # gems match to the right
                                    if c < COLUMNS - 2:
                                        if r > 0:
                                            if ng[r,c] == ng[diagUp_right_gem]:
                                                moves_remain_list = [gem_at(r,c), 
                                                                    gem_at(right1_gem[0],right1_gem[1]),
                                                                    gem_at(diagUp_right_gem[0], diagUp_right_gem[1])]
                                                return (moves_remain_list)

                                        if r < ROWS - 1:
                                            if ng[r,c] == ng[diagDown_right_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                    gem_at(right1_gem[0],right1_gem[1]),
                                                                    gem_at(diagDown_right_gem[0], diagDown_right_gem[1])]
                                                return (moves_remain_list)
                                    
                                    # gems match one over
                                    if c < COLUMNS - 3:
                                        if ng[r,c] == ng[right1_over_gem]:
                                            moves_remain_list = [gem_at(r,c),
                                                                gem_at(right1_gem[0],right1_gem[1]),
                                                                gem_at(right1_over_gem[0], right1_over_gem[1])]
                                            return (moves_remain_list)

                                    if c > 1:
                                        if ng[r,c] == ng[left1_over_gem]:
                                            moves_remain_list = [gem_at(r,c),
                                                                gem_at(right1_gem[0],right1_gem[1]),
                                                                gem_at(left1_over_gem[0], left1_over_gem[1])]
                                            return (moves_remain_list)

                                    # gems match to the left
                                    if c > 0:
                                        if r > 0:
                                            if ng[r,c] == ng[diagUp_left_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(right1_gem[0],right1_gem[1]),
                                                                gem_at(diagUp_left_gem[0], diagUp_left_gem[1])]
                                                return (moves_remain_list)

                                        if r < ROWS - 1:
                                            if ng[r,c] == ng[diagDown_left_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(right1_gem[0],right1_gem[1]),
                                                                gem_at(diagDown_left_gem[0], diagDown_left_gem[1])]
                                                return (moves_remain_list)                                          
                            
                            # # gems match triangles    
                            if c < COLUMNS - 2:
                                if r < ROWS - 1:
                                    if ng[r,c] == ng[triangle_down_gem] == ng[right2_gem]:
                                        moves_remain_list = [gem_at(r,c),
                                                                gem_at(triangle_down_gem[0],triangle_down_gem[1]),
                                                                gem_at(right2_gem[0], right2_gem[1])]
                                        return (moves_remain_list) 

                                if r > 0: 
                                    if ng[r,c] == ng[triangle_up_gem] == ng[right2_gem]:
                                        moves_remain_list = [gem_at(r,c),
                                                                gem_at(triangle_up_gem[0],triangle_up_gem[1]),
                                                                gem_at(right2_gem[0], right2_gem[1])]
                                        return (moves_remain_list) 

                            # check vertical 
                            down1_gem = (r + 1, c)
                            down1_over_gem = (r + 3, c)
                            up1_over_gem = (r - 2, c)

                            diagUp_left_gem = (r - 1, c - 1)
                            diagUp_right_gem = (r - 1, c + 1)

                            diagDown_left_gem = (r + 2, c - 1)
                            diagDown_right_gem = (r + 2, c + 1)

                            down2_gem = (r + 2, c)
                            triangle_left_gem = (r + 1, c - 1)
                            triangle_right_gem = (r + 1, c + 1)

                            if r < ROWS - 1:
                                if ng[r,c] == ng[down1_gem]:
                                    # gem_at(r, c).center_y  += 10
                                    # gem_at(down1_gem[0],down1_gem[1]).center_y += 10

                                    # gems match down below
                                    if r < ROWS - 2:
                                        if c < COLUMNS - 1:
                                            if ng[r,c] == ng[diagDown_right_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(diagDown_right_gem[0], diagDown_right_gem[1])]
                                                return (moves_remain_list) 

                                        if c > 0:
                                            if ng[r,c] == ng[diagDown_left_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(diagDown_left_gem[0], diagDown_left_gem[1])]
                                                return (moves_remain_list)

                                    # gems match one up or down
                                    if r < ROWS - 3:
                                        if ng[r,c] == ng[down1_over_gem]:
                                            moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(down1_over_gem[0], down1_over_gem[1])]
                                            return (moves_remain_list)

                                    if r > 1: 
                                        if ng[r,c] == ng[up1_over_gem]:
                                            moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(up1_over_gem[0], up1_over_gem[1])]
                                            return (moves_remain_list)

                                    # gems match up above
                                    if r > 0:
                                        if c < COLUMNS - 1:
                                            if ng[r,c] == ng[diagUp_right_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(diagUp_right_gem[0], diagUp_right_gem[1])]
                                                return (moves_remain_list)

                                        if c > 0:
                                            if ng[r,c] == ng[diagUp_left_gem]:
                                                moves_remain_list = [gem_at(r,c),
                                                                gem_at(down1_gem[0],down1_gem[1]),
                                                                gem_at(diagUp_left_gem[0], diagUp_left_gem[1])]
                                                return (moves_remain_list)

                            # gems match triangles 
                            if r < ROWS - 2:
                                if c < COLUMNS - 1:
                                    if ng[r,c] == ng[triangle_right_gem] == ng[down2_gem]:
                                        moves_remain_list = [gem_at(r,c),
                                                                gem_at(triangle_right_gem[0],triangle_right_gem[1]),
                                                                gem_at(down2_gem[0], down2_gem[1])]
                                        return (moves_remain_list)

                                if c > 0:
                                    if ng[r,c] == ng[triangle_left_gem] == ng[down2_gem]:
                                        moves_remain_list = [gem_at(r,c),
                                                                gem_at(triangle_left_gem[0],triangle_left_gem[1]),
                                                                gem_at(down2_gem[0], down2_gem[1])]
                                        return (moves_remain_list)

                    return (moves_remain_list)           



        def game_controller():


            # okay, this is the main loop. 
            # this  controls the state of the game as elegantly and simply as possible

            # first, often used functions in the main loop. . . 
            def do_gem_drop():
                for gem in self.gem_list:
                    if gem.state == "waiting to fall":
                        if random.random() >= self.drop_jitter:
                            gem.state = "falling"
                    
                    elif gem.state == "falling":
                        gem.speed *= ACCELERATION 
                        move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                        move_towards_point(gem, [move_to_x, move_to_y])
                        if gem.speed == 0:
                            gem.state = "bouncing dip"
                            gem.speed = 1

                    elif gem.state == "bouncing dip":
                        gem.center_y -= 3
                        move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                        if gem.center_y <= move_to_y - 10:
                            gem.state = "bouncing up"
                    elif gem.state == "bouncing up":
                        gem.center_y += 3
                        move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                        if gem.center_y >= move_to_y :
                            gem.state = "idle"
                            gem.speed = 0

            # the game states are:
            # 0) initialize. - allowes the printed gem grid to fall into place and then moves to 'waiting for player'
            if self.game_state == "initializing":
                
                do_gem_drop()
                if not self.are_gems_moving():
                    for gem in self.gem_list:
                        gem.inspect_matches = False
                    self.gem_to_move = None
                    self.gem_being_moved = None
                    self.game_state = "check for player moves"
            
            # 3) gems switching places - two gems switch places (gem to move, gem being moved)
            elif self.game_state == "gems switching":
                # turn off the blinking from the previous "waiting for player" state
                self.wait_timer = 0
                self.moves_remain_list = []

                # now, if the gem to move or gem being moved is a flashing 5Gem,
                # then destroy everything that is the same color as the gem being moved or the gem to move
                if self.gem_to_move.index == 99:
                    self.gem_to_move.is_matched = True
                    gem1 = self.gem_to_move
                    
                    if gem1.direction == "right":
                        gem1.column -= 1
                    if gem1.direction == "left":
                        gem1.column += 1
                    if gem1.direction == "up":
                        gem1.row += 1
                    if gem1.direction == "down":
                        gem1.row -= 1

                    gem2 = self.gem_being_moved
                    gem2.speed = GEM_SPEED / 3
                    if gem1.direction == "right":
                        gem2.column += 1
                    if gem1.direction == "left":
                        gem2.column -=1
                    if gem1.direction == "up":
                        gem2.row -= 1
                    if gem1.direction == "down":
                        gem2.row += 1

                    self.destroy_gem_index = gem2.index
                    self.game_state = "detonate special gems"

                else:
                    gem = self.gem_to_move
                    gem.speed = GEM_SPEED / 3
                    self.foreground_gem_list.append(gem)
                    self.gem_list.remove(gem)
                    # print(gem.direction)

                    gem = self.gem_being_moved
                    gem.speed = GEM_SPEED / 3

                    self.game_state = "gems switching loop"

            elif self.game_state == "gems switching loop":
                gem = self.gem_to_move
                gem.speed *= ACCELERATION 
                move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                move_towards_point(gem, [move_to_x, move_to_y])
                # move_towards_point(gem, [100, 100], 10)
                if gem.speed == 0:
                    gem.inspect_matches = True
                    self.number_grid[gem.row, gem.column] = gem.index
                
                gem = self.gem_being_moved
                gem.speed *= ACCELERATION 
                move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                move_towards_point(gem, [move_to_x, move_to_y])
                if gem.speed == 0:
                    gem.inspect_matches = True
                    self.number_grid[gem.row, gem.column] = gem.index

                    ## is the free-range swiching option activated? 
                    if self.switch_free_range_mode == True:
                        for gem in self.gem_list:
                            for gem in self.foreground_gem_list:
                                self.gem_list.append(gem)
                                self.foreground_gem_list.remove(gem)
                        gem.inspect_matches = False
                        self.gem_to_move = None
                        self.gem_being_moved = None
                        self.game_state = "check for player moves"

                    ## free range switching option is not activated... 
                    else:
                        self.game_state = "checking for matches after switch"
                    # print(self.number_grid)

            # 4) check switched gem for matches - check each of the switched gems to see if there are any matches.
            #    if there are no matches, move to 'gems switching back'
            #    else move to 'mark matched special gems'
            elif self.game_state == "checking for matches after switch":
                check_this_gem = self.are_matches_in_number_grid(self.number_grid)

                if check_this_gem == True:
                    
                    self.gem_list.append(self.gem_to_move)
                    self.foreground_gem_list.remove(self.gem_to_move)
                    self.game_state = "mark matched special gems"

                else:
                    self.game_state = "gems switching back"

            # 5) mark matched special gems. mark all matched gems. set any gems in 4 or 5 gmes with new col, row info so that they can move towards their 
            #    forming gems. mark the number_grid with zeroes under the matches. 
            elif self.game_state == "mark matched special gems":

                check_for_special_matches()


                self.game_state = "mark matched gems"

            # 5.5) mark matched (regular) gems. mark all matched gems. set any gems in 4 or 5 somes with new col, row info so that they can move towards their 
            #    forming gems. mark the number_grid with zeroes under the matches. 
            elif self.game_state == "mark matched gems":
                check_regular_matches()

                self.game_state = "move and remove matched gems"
            
            # 6) move and remove matched gems. 
            # First, copy any gems that are the source of 4 or 5 matched gems to the 
            # foreground layer, too, but set their speed to 0. Leave their 'follower' gems 
            # on the gem_layer, so they will slide underneath these 'master' gems on the  
            elif self.game_state == "move and remove matched gems":
                for i in range(3):
                    for gem in self.gem_list:

                        if gem.is_matched == True:
                            gem.speed = GEM_SPEED
                            self.number_grid[gem.row, gem.column] = 0

                    self.game_state = "move and remove matched gems loop - make gems"

            elif self.game_state == "move and remove matched gems loop - make gems":
                # do stuff for 5gem and 5gem followers. 5gem is on foreground layer.
                # 5 gem followers
                for gem in self.gem_list:
                    if gem.category == "gem_follower":
                        if gem.speed != 0:
                            move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                            move_towards_point(gem, [move_to_x, move_to_y])
                        else:
                            gem.kill()

                are_any_follower_gems_left = False

                for follower_gem in self.gem_list:
                    if follower_gem.category == "gem_follower":
                        are_any_follower_gems_left = True

                ### okay, once the follower gems are all gone, we'll make new 5Gems, 4Gems, and CrossGems...

                if not are_any_follower_gems_left:
                    for i in range (3):
                        for gem in self.foreground_gem_list:
                            if gem.category == "proto_5Gem":
                                
                                gem.index = 99
                                self.number_grid[gem.row, gem.column] = 99
                                gem.speed = 0
                                gem.is_matched = False
                                gem.category= "5Gem"
                                self.gem_list.append(gem)
                                self.foreground_gem_list.remove(gem)
                                gem.scale = 1.6

                            if gem.category == "proto_4Gem":
                            
                                self.number_grid[gem.row, gem.column] = gem.index
                                gem.speed = 0
                                gem.is_matched = False
                                gem.category = "4Gem"

                                self.gem_list.append(gem)
                                self.foreground_gem_list.remove(gem)

                            if gem.category == "proto_CrossGem":
                            
                                self.number_grid[gem.row, gem.column] = gem.index
                                gem.speed = 0
                                gem.is_matched = False
                                gem.category = "CrossGem"

                                self.gem_list.append(gem)
                                self.foreground_gem_list.remove(gem)

                    self.game_state = "detonate special gems"

            ### once we've made all of the 5Gems, 4Gems, and CrossGems, let's activate
            ### 5Gem Bombs, 4Gem Bombs, and CrossGem Bombs
            elif self.game_state == "detonate special gems":

                for check_gem in self.gem_list:

                    ### Do 5Gem bombs - mark affected bomb gems as matched, but don't animate yet
                    if check_gem.category == "5Gem" and check_gem.is_matched: 
                        check_gem.category = "5Gem_bomb"
                        check_gem.speed = GEM_SPEED

                        for this_bomb_gem in self.gem_list: 

                            ### mark all gems of the same color as the gem the 5Gem touched          
                            if this_bomb_gem.index == self.destroy_gem_index:
                                if this_bomb_gem.category == None:
                                    
                                    this_bomb_gem.category = "5Gem_bomb"
                                    this_bomb_gem.speed = GEM_SPEED
                                    this_bomb_gem.is_matched = True
                                    ### delete below
                                    # this_bomb_gem.scale = 1.3
                                
                                elif this_bomb_gem.category == "CrossGem":

                                    this_bomb_gem.is_matched = True

                                elif this_bomb_gem.category == "4Gem":

                                    this_bomb_gem.is_matched = True

                for check_gem in self.gem_list:
                    ### Do CrossGem bombs - mark affected bomb gems as matched, but don't animate yet
                    if check_gem.category == "CrossGem" and check_gem.is_matched:
                        self.destroy_gem_index = check_gem.index
                        check_gem.category = "CrossGem_bomb"
                        
                        # Mark CrossGem bombs in a cross format from with the check_gem as the origin
                        for cross_gem in self.gem_list:
                            if cross_gem.row == check_gem.row or cross_gem.column == check_gem.column:
                                if cross_gem.category == None:
                                    cross_gem.category = "CrossGem_bomb"
                                cross_gem.is_matched = True

                for check_gem in self.gem_list:                            
                    ### Do 4Gem bombs - mark affected bomb gems as matched, but don't animate yet
                    if check_gem.category == "4Gem" and check_gem.is_matched:  
                        self.destroy_gem_index = check_gem.index 

                        def do_4Gem_bomb(this_gem):  

                            if this_gem.category == None or this_gem.category == "4Gem":                     
                                this_gem.category = "4Gem_bomb"

                                this_gem.scale = 1.5
                                this_gem.speed = GEM_SPEED
                            if this_gem.category == "5Gem":
                                this_gem.update_animation()

                            this_gem.is_matched = True

                            
                        do_4Gem_bomb(check_gem)
                        if check_gem.row > 0: # gem above
                            do_4Gem_bomb(gem_at(check_gem.row - 1, check_gem.column))
                        if check_gem.row > 0 and check_gem.column < COLUMNS - 1: # gem above and to the right
                            do_4Gem_bomb(gem_at(check_gem.row - 1, check_gem.column + 1))
                        if check_gem.column < COLUMNS - 1: # gem to the right
                            do_4Gem_bomb(gem_at(check_gem.row, check_gem.column + 1))
                        if check_gem.row < ROWS - 1 and check_gem.column < COLUMNS - 1: # gem to the right and down
                            do_4Gem_bomb(gem_at(check_gem.row + 1, check_gem.column + 1))
                        if check_gem.row < ROWS - 1: # gem below
                            do_4Gem_bomb(gem_at(check_gem.row + 1, check_gem.column))
                        if check_gem.row < ROWS - 1 and check_gem.column > 0: # gem to the left and down
                            do_4Gem_bomb(gem_at(check_gem.row + 1, check_gem.column - 1))
                        if check_gem.column > 0: # gem to the left
                            do_4Gem_bomb(gem_at(check_gem.row, check_gem.column - 1))
                        if check_gem.row > 0 and check_gem.column > 0: # gem to the left and above
                            do_4Gem_bomb(gem_at(check_gem.row - 1, check_gem.column - 1))

                are_there_any_special_gems_that_are_matched = False
                for gem in self.gem_list:
                    if gem.is_matched == True:
                        if gem.category == "5Gem" or gem.category == "4Gem" or gem.category == "CrossGem":
                            are_there_any_special_gems_that_are_matched = True
                
                if not are_there_any_special_gems_that_are_matched:
                    for i in range (3):
                        for gem in self.gem_list:
                            if gem.category == "5Gem_bomb" or gem.category == "4Gem_bomb" or gem.category == "CrossGem_bomb":
                                self.foreground_gem_list.append(gem)
                                self.gem_list.remove(gem)
                        self.game_state = "detonate special gems - animate"         
                else: 
                    self.game_state = "detonate special gems"           

            # now animate the blowing up of all the special gems
            elif self.game_state == "detonate special gems - animate":
                for check_gem in self.foreground_gem_list:

                    ### Now animate 4Gem bombs
                    if check_gem.category == "4Gem_bomb" and check_gem.is_matched:  
                        check_gem.scale -= 0.02
                        if check_gem.scale < 1:

                            check_gem.category = "moving to be destroyed"
                            self.number_grid[check_gem.row, check_gem.column] = 0

                    ### Now animate 5Gem bombs
                    if check_gem.category == "5Gem_bomb" and check_gem.is_matched: 

                        def shake_gem(gem):
                            rand_x = random.randint(1, 10) - 5
                            rand_y = random.randint(1, 10) - 5
                            this_x, this_y = trans_cr_to_xy(gem.column, gem.row)
                            gem.center_x = this_x + rand_x
                            gem.center_y = this_y + rand_y
                            gem.scale += 0.006
                            if gem.scale > 1.2:
                                if random.random() >= .5:
                                    gem.scale = 1
                                    gem.center_x = this_x
                                    gem.center_y = this_y

                                    self.number_grid[gem.row, gem.column] = 0
                                    gem.category = "moving to be destroyed"
                                else:
                                    gem.scale = 1.2
                            if gem.index == 99:
                                gem.update_animation() 

                        shake_gem(check_gem)

                    ### Now animate CrossGem bombs
                    if check_gem.category == "CrossGem_bomb" and check_gem.is_matched: 

                        def rattle_gem(gem):
                            rand_scale = (random.randint(1, 4) - 2) / 10 

                            gem.scale = 1 + rand_scale
                            gem.timer += 1
                            if gem.timer > 50:
                                if random.random() >= .5:
                                    gem.scale = 1

                                    self.number_grid[gem.row, gem.column] = 0
                                    gem.category = "moving to be destroyed"

                            if gem.index == 99:
                                gem.update_animation() 

                        rattle_gem(check_gem)

                are_any_bomb_gems_left = False

                for bomb_gem in self.foreground_gem_list:
                    if (bomb_gem.category == "4Gem_bomb" or bomb_gem.category == "5Gem_bomb"
                      or bomb_gem.category == "CrossGem_bomb"):
                        are_any_bomb_gems_left = True

                if not are_any_bomb_gems_left:

                        self.game_state = "destroy matched gems"

            ### Do 5Gem bombs - what happens when 5Gems are triggered/matched

            # 7) destroy matched gems. 
            elif self.game_state == "destroy matched gems":

                # finally, mark all the None-type gems that are marke as .is_matched so that they move off the game grid
                for i in range(3):
                    for gem in self.gem_list:
                        # transfer moving gem to foreground list so it's in front of the game gems
                        if gem.category == None and gem.is_matched:
                            self.foreground_gem_list.append(gem)
                            self.gem_list.remove(gem)    
                            gem.category = "moving to be destroyed"
 
                self.game_state = "new gems fall"

            # 8) let new gems fall. pack down zeroes. pack all zeroes down in the number grid. generate new gems and let them fall into place. 
            elif self.game_state == "new gems fall":
                # elif self.game_state == "trigger gems falling":
                # find out how many zeroes, if any, are directly below a gem
                # then reassign a new row to it so the gem can fall to the new row
                for i in range(20):
                    # now check below gems to see if therer are any empty spaces
                    # by checking the zeroes in the number_grid
                    for gem in self.gem_list:
                        if gem.row < (ROWS - 1):
                            while gem.row < (ROWS - 1):
                                if self.number_grid[gem.row + 1, gem.column] == 0:
                                    self.number_grid[gem.row, gem.column] = 0
                                    gem.row += 1
                                    self.number_grid[gem.row, gem.column] = gem.index 
                                    gem.speed = GEM_SPEED
                                    gem.state = "ready to fall after match"
                                    gem.inspect_matches = True
                                else:
                                    break
                # print (self.number_grid)
                # okay, now that we've flushed all the zero values to the top of 
                # number_grid, let's fill in the zeroes with new gems          
                for r in range (ROWS):
                    for c in range (COLUMNS):
                        if self.number_grid[r, c] == 0:
                            self.drop_jitter = .30
                            self.create_gem(r, c)

                                                        
                # print (self.number_grid)
                self.game_state = "new gems fall loop"    

            elif self.game_state == "new gems fall loop":
                for gem in self.gem_list:
                    this_x, this_y = trans_cr_to_xy(gem.column, gem.row)
                    if gem.state == "ready to fall after match":
                        gem.state = "falling"

                do_gem_drop()
                if not self.are_gems_moving():
                    self.game_state = "checking for matches after fall"

            # 9) check fallen gems for matches. See if we can tie this back to the loop at # 4. if no matches, 'waiting for player' 
            elif self.game_state == "checking for matches after fall":
                check_this_gem = self.are_matches_in_number_grid(self.number_grid)

                if check_this_gem == True:

                    self.game_state = "mark matched special gems"
                    
                else:
                    self.gem_to_move = None
                    self.gem_being_moved = None
                    for gem in self.gem_list:
                        gem.inspect_matches = False
                    self.game_state = "check for player moves"

            # 10) gems switching back. make the marked gems switch back if there are no matches. then go to 'waiting for player'
            elif self.game_state == "gems switching back":
                gem1 = self.gem_to_move
                gem1.speed = GEM_SPEED / 3
                if gem1.direction == "right":
                    gem1.column -= 1
                if gem1.direction == "left":
                    gem1.column += 1
                if gem1.direction == "up":
                    gem1.row += 1
                if gem1.direction == "down":
                    gem1.row -= 1
                # print(gem.direction)

                gem2 = self.gem_being_moved
                gem2.speed = GEM_SPEED / 3
                if gem1.direction == "right":
                    gem2.column += 1
                if gem1.direction == "left":
                    gem2.column -=1
                if gem1.direction == "up":
                    gem2.row -= 1
                if gem1.direction == "down":
                    gem2.row += 1

                self.game_state = "gems switching back loop"

            elif self.game_state == "gems switching back loop":
                gem = self.gem_to_move
                gem.speed *= ACCELERATION 
                move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                move_towards_point(gem, [move_to_x, move_to_y])
                if gem.speed == 0:
                    gem.inspect_matches = False
                    self.number_grid[gem.row, gem.column] = gem.index
                    if gem in self.foreground_gem_list:
                        self.gem_list.append(gem)
                        self.foreground_gem_list.remove(gem)
                
                gem = self.gem_being_moved
                gem.speed *= ACCELERATION 
                move_to_x, move_to_y = trans_cr_to_xy(gem.column, gem.row)
                move_towards_point(gem, [move_to_x, move_to_y])
                if gem.speed == 0:
                    self.number_grid[gem.row, gem.column] = gem.index
                    gem.inspect_matches = False
                    self.gem_to_move = None
                    self.gem_being_moved = None
                    self.game_state = "waiting for player"

            elif self.game_state == "check for player moves":

                self.moves_remain_list = check_player_moves_available()

                # print(moves_remain) 
                if self.moves_remain_list == []:
                    # print(self.moves_remain_list)
                    self.game_state = "No Moves Left..."
                else:
                    # print(self.moves_remain_list)
                    self.game_state = "waiting for player"

            # 10.5 do game pausing stuff
            if self.game_state == "pausing game":
                pass

            # 11) Finally, a bit for waiting for player
            if self.game_state == "waiting for player":
                self.wait_timer += 1
                pause_sec_before_blinking = 3 
                if self.wait_timer > pause_sec_before_blinking * 60:
                    # if self.moves_remain_list != []:
                    for gem in self.moves_remain_list:
                        if (self.wait_timer > pause_sec_before_blinking * 60 and
                            self.wait_timer < (pause_sec_before_blinking * 60) + 10):
                            gem.alpha = 150
                        if self.wait_timer > (pause_sec_before_blinking * 60) + 30:
                            gem.alpha = 255
                        if self.wait_timer > (pause_sec_before_blinking * 60) + 80:
                            self.wait_timer = pause_sec_before_blinking * 60



    # TODO: 
    # fix 5gem and 4 gem grab all effects
    # start game screen
    # add music
    # add sound fx


    

        # ***************************************************
        #               END GAME CONTROLLER
        # ***************************************************

        game_controller()

        if self.game_state != "pausing game":
            self.gem_list.update()
            self.gem_list.update_animation()
            self.foreground_gem_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # reset game
        if key == arcade.key.SPACE:
            MyGame.setup(self)

        # switch to free-range gem mode
        if key == arcade.key.D:
            if self.switch_free_range_mode == False:
                self.switch_free_range_mode = True
            else: 
                self.switch_free_range_mode = False

        # # slow motion mode  
        # if key == arcade.key.E:
        #     if self.GEM_SPEED == 10:
        #         self.GEM_SPEED = 2
        #         self.ACCELERATION = 1
        #     else:
        #         self.GEM_SPEED = 10
        #         self.ACCELERATION = 1.06

        # Pause activate / deactivate
        if key == arcade.key.ESCAPE:
            if self.PAUSE == False:
                self.PAUSE = True
                self.game_state_temp = self.game_state
                self.game_state = "pausing game"
            else:
                self.PAUSE = False
                self.game_state = self.game_state_temp

            



        # this whole thing with adding new columns needs work because
        # well, it's just not working right now. All the new zeroed gems fall on top of column one insead of one column to the right
        # maybe fix this later. 
        if key == arcade.key.A:
            self.number_grid, COLUMNS = MyGame.add_columns(self.number_grid, self.gem_list)
            print(self.number_grid, COLUMNS)
        
        if key == arcade.key.S:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.mouse_pointer_sprite.center_x = x
        self.mouse_pointer_sprite.center_y = y
        self.mouse_pointer_active_sprite.center_x = x - 20
        self.mouse_pointer_active_sprite.center_y = y + 26
  
    def get_mouse_direction(self, start_x, start_y, end_x, end_y):

        # determine direction of mouse drag (or two gem pick) 
        direction = ""

        # myradians = math.atan2(self.mouse_release_y - self.mouse_press_y, self.mouse_release_x - self.mouse_press_x)
        myradians = math.atan2(end_y - start_y, end_x - start_x)
        mydegrees = int(math.degrees(myradians))
        # print(mydegrees)

        if mydegrees < 45 and mydegrees >= -45:
            if self.gem_to_move.column < COLUMNS - 1:
                direction = "right"

        elif mydegrees < -45 and mydegrees >= - 135:
            if self.gem_to_move.row < ROWS - 1:
                direction = "down"

        elif mydegrees < -135 or mydegrees >= 135:
            if self.gem_to_move.column > 0:
                direction = "left"
    
        elif mydegrees < 135 and mydegrees >=45:
            if self.gem_to_move.row > 0:
                direction = "up"

        return direction


    def is_gem_adjacent(self):
        adjacent = False
        if self.gem_to_move.direction == "left":
            if (self.gem_to_move.column - 1 == self.gem_being_moved.column and
                self.gem_to_move.row == self.gem_being_moved.row):
                adjacent = True
        if self.gem_to_move.direction == "right":
            if (self.gem_to_move.column + 1 == self.gem_being_moved.column and
                self.gem_to_move.row == self.gem_being_moved.row):
                adjacent = True
        if self.gem_to_move.direction == "up":
            if (self.gem_to_move.row - 1 == self.gem_being_moved.row and
                self.gem_to_move.column == self.gem_being_moved.column):
                adjacent = True
        if self.gem_to_move.direction == "down":
            if (self.gem_to_move.row + 1 == self.gem_being_moved.row and
                self.gem_to_move.column == self.gem_being_moved.column):
                adjacent = True

        return adjacent

    # switch column, row values of gem_to_move and gem_being_moved    
    def switch_gems_columns_and_rows(self):
        direction = self.gem_to_move.direction

        if direction == "left":
            self.gem_to_move.column -= 1
            self.gem_being_moved.column +=1

        if direction == "right":
            self.gem_to_move.column += 1
            self.gem_being_moved.column -= 1

        if direction == "up":
            self.gem_to_move.row -= 1
            self.gem_being_moved.row += 1
            
        if direction == "down":
            self.gem_to_move.row += 1
            self.gem_being_moved.row -= 1

    # switch column, row values of gem_to_move and gem_being_moved    
    def switch_gem_to_move_columns_and_rows(self):
        direction = self.gem_to_move.direction

        if direction == "left":
            self.gem_to_move.column -= 1

        if direction == "right":
            self.gem_to_move.column += 1

        if direction == "up":
            self.gem_to_move.row -= 1
            
        if direction == "down":
            self.gem_to_move.row += 1

    # switch column, row values of gem_to_move and gem_being_moved    
    def switch_gem_being_moved_columns_and_rows(self):
        direction = self.gem_to_move.direction

        if direction == "left":
            self.gem_being_moved.column +=1

        if direction == "right":
            self.gem_being_moved.column -= 1

        if direction == "up":
            self.gem_being_moved.row += 1
            
        if direction == "down":
            self.gem_being_moved.row -= 1

    def on_mouse_press(self, x, y, button, key_modifiers):
            """
            Called when the user presses a mouse button.
            """



            if (self.game_state == "waiting for player"):
                self.mouse_press_x = x
                self.mouse_press_y = y
                # print(x,y)
                # so need to 'mark' a gem to move
                gem_hit_list = arcade.check_for_collision_with_list(self.mouse_pointer_active_sprite, self.gem_list)
                for gem in gem_hit_list:
                    # make all gems stop blinking
                    for alpha_gem in self.gem_list:
                        alpha_gem.alpha = 255
                        self.wait_timer = 0

                    if self.gem_to_move:
                        self.gem_being_moved = gem
                    else:
                        self.gem_to_move = gem

                if gem_hit_list == []:
                    # print("no second gem")
                    self.gem_to_move = None
                    self.gem_being_moved = None

                # print (self.gem_to_move, self.gem_being_moved)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        # do the two-gem select method
        if (self.game_state == "waiting for player" and self.gem_to_move and self.gem_being_moved):
            # get direction
            self.gem_to_move.direction = self.get_mouse_direction(self.gem_to_move.center_x, self.gem_to_move.center_y,
                                                                self.gem_being_moved.center_x, self.gem_being_moved.center_y)
            # print (self.gem_to_move.direction)
            
            # find out if gems are adjacent
            adjacent = self.is_gem_adjacent()
            #print (self.gem_to_move.column, self.gem_being_moved.column, adjacent)

            # if adjacent, switch gems
            if adjacent:
                self.switch_gems_columns_and_rows()
                self.game_state = "gems switching"
            else:
                self.gem_to_move = None
                self.gem_being_moved = None

        # do the click-and-drag method
        elif (self.game_state == "waiting for player" and self.gem_to_move and not self.gem_being_moved):
            self.mouse_release_x = x
            self.mouse_release_y = y

            # I don't fucking know why, but experiment produces a distance error of +27x and -32 y, 
            # so I'm correcting for this here for now. . . grrr...
            # I suspect it's not actually 'center_x' but 'upper_left_corner_x' of the image. . . 
            # print (self.gem_to_move.center_x + 27, self.gem_to_move.center_y - 32)
            
            # getting the distance allows for us to not trigger moving if the mouse click and mouse release are 
            # only a few pixels apart. . . 
            this_distance = (get_dist_between_points([self.gem_to_move.center_x + 27, 
                            self.gem_to_move.center_y - 32], [x, y]))
            # print(this_distance)

            self.gem_to_move.direction = self.get_mouse_direction(self.mouse_press_x, self.mouse_press_y,   
                                                                self.mouse_release_x, self.mouse_release_y)
            # print(self.gem_to_move.direction)

            # if moving_within_game_board and this_distance > 32 (for click-drag):
            if this_distance > 32:

                self.switch_gem_to_move_columns_and_rows()
                # ... and move the second gem. The one we're trading places with . . . 
                for gem in self.gem_list:
                    test_x, test_y = trans_cr_to_xy(self.gem_to_move.column, self.gem_to_move.row)
                    if gem.collides_with_point(tuple([test_x, test_y])) and gem != self.gem_to_move:
                        self.gem_being_moved = gem
                # print(self.gem_to_move, self.gem_being_moved)
                self.switch_gem_being_moved_columns_and_rows()
                self.game_state = "gems switching"


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()