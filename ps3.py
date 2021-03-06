# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        self.dirt = dirt_amount
        # this creates a dictionary with all the tiles and their dirt amounts in them. it goes row
        # by row and adds the tiles that way. This was not explicitly instructed, but they said:
        # "If you find any places above where the specification of the simulation dynamics seems
        # ambiguouss, it is up to you to make a reasonable decision about how your program/model will
        # behave, and document that decision in your code."
        # while they did specify that the tiles should be ordered pairs on ints (w,h), they didn't
        # specify how to store all the tiles or how to keep track of the dirt on the tiles. Making 
        # a dictionary to store the tiles and making their dirt the value seemed like a reasonable
        # solution
        col = 0
        row = 0
        tiles = {}
        for i in range(self.width * self.height):
            tiles[(row, col)] = (self.dirt)
            col += 1
            if col == self.height:
                col = 0
                row += 1
        self.tiles = tiles
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        if self.tiles[math.floor(pos.get_x()), math.floor(pos.get_y())] - capacity >= 0:
            self.tiles[math.floor(pos.get_x()), math.floor(pos.get_y())] -= capacity
        else:
            self.tiles[math.floor(pos.get_x()), math.floor(pos.get_y())] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return(self.tiles[m,n] == 0)
        
    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        clean_tiles = 0
        for tile in self.tiles:
            if self.tiles[tile] == 0:
                clean_tiles += 1
        return(clean_tiles)
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        
        return((math.floor(pos.get_x()), math.floor(pos.get_y())) in self.tiles)
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return(self.tiles[(m,n)])
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.cap = capacity
        self.angle = random.uniform(0.0, 360.0)
        # random_pos = room.get_random_position()
        # if room.is_position_valid(random_pos)
        self.pos = room.get_random_position()

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return(self.pos)

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return(self.angle)

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.pos = position
        
    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.angle = direction
        
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the
        tile it is on as having been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError




# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return(self.width * self.height)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        return(self.is_position_in_room(pos))
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return(Position(random.uniform(0.0, self.width), random.uniform(0.0, self.height)))





class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        return((m,n) in self.furniture_tiles)
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        return(self.is_tile_furnished(math.floor(pos.get_x()), math.floor(pos.get_y())))
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        return((not self.is_position_furnished(pos)) and self.is_position_in_room(pos))
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return(self.width * self.height - len(self.furniture_tiles))
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room 
        and not in a furnished area).
        """
        end = False
        while not end:
            ran_pos=Position(random.uniform(0.0,self.height+0.999),random.uniform(0.0,self.width+0.999))
            if self.is_position_valid(ran_pos):
                end = True
        return(ran_pos)



# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        new_position = self.pos.get_new_position(self.angle, self.speed)
        if self.room.is_position_valid(new_position):
            self.pos = new_position
            self.room.clean_tile_at_position(self.pos, self.cap)
        else:
            self.angle = random.uniform(0.0, 360.0)
# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)



# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        new_position = self.pos.get_new_position(self.angle, self.speed)
        if self.gets_faulty() or not self.room.is_position_valid(new_position):
            self.angle = random.uniform(0.0, 360.0) 
        else:
                self.pos = new_position
                self.room.clean_tile_at_position(self.pos, self.cap)
#test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """

   
    # checks to see if the trials should be animated. comment out this line to get rid of the animated check 
    # animated = input('animate? y or n or d (default settings)')
    # uses a try except to check if the line assigning animated has been commented out
    try:
        animated == 'y'
    except:
        animated = 'n'
    # gets values for animation
    if animated == 'y':
        if input('is furnished, t or f') == 't':
            is_furnished = True
        else:
            is_furnished = False
        delay = float(input('delay. float. default is 0.03. higher number will go slower'))
        anim = ps3_visualize.RobotVisualization(num_robots, width, height, is_furnished, delay)
    elif animated == 'd':
        is_furnished = False
        delay = 0.03
        anim = ps3_visualize.RobotVisualization(num_robots, width, height, is_furnished, delay)
        animated = 'y'
    number_of_trials = []
    # the main loop which runs over the code for each individual trial
    for i in range(num_trials):
        room = EmptyRoom(width, height, dirt_amount)
        if animated == 'y':
            if is_furnished == True:
                room = FurnishedRoom(width, height, dirt_amount)
                room.add_furniture_to_room()
        time = 0
        robot_list = []
        for i in range(num_robots):
            robot_list += [robot_type(room, speed, capacity)]
        # the code for each trial. they will continue until the room is sufficently clean
        while room.get_num_cleaned_tiles() / room.get_num_tiles() < min_coverage:
            for robot in robot_list:
                robot.update_position_and_clean()
                room = robot.room
            time += 1
            if animated == 'y':
                anim.update(room, robot_list)
        number_of_trials += [time]
    if animated == 'y':
        anim.done()
    # returns the average time ticks per trial
    return(sum(number_of_trials)/len(number_of_trials))

def test_random_prob(num_trials):
    good = 0
    trials_list = []
    trials = 0
    for i in range(num_trials):
        trials += 1
        end = 8
        random_number = random.uniform(0.0, 360.0)
        if random_number > 40 and random_number < 140:
            good += 1
        if good == end:
            trials_list += [trials]
    return(sum(trials_list)/len(trials_list))

def test_work():
    # random.seed()
    
    print(run_simulation(1, 1, 1, 4, 4, 2, 0.5, 2, StandardRobot))

    
    # print(test_random_prob(1000))
    
    recroomt1 = RectangularRoom(3,4,2)
    eroomt1 = EmptyRoom(3,4,2)
    cleanroom = EmptyRoom(5,5,0)
    froomt1 = FurnishedRoom(3,4,2)
    erobott1 = Robot(eroomt1, 1, 1)
    frobott1 = Robot(froomt1, 1, 1)
    srobott1 = StandardRobot(eroomt1, 1, 1)
    srobott2 = StandardRobot(eroomt1, 2, 1)    
    srobott3 = StandardRobot(cleanroom, 1, 2)
    srobott4 = StandardRobot(froomt1, 1, 1)
    flrobott1 = FaultyRobot(eroomt1, 1, 1)
    flrobott2 = FaultyRobot(froomt1, 1, 1)
    
    position_test1 = Position(1.7,2.1)
    position_test2 = Position(2.0,3.9)
    position_test3 = Position(0.0,0.0)
    position_test4 = Position(4.0,0.0)
    position_test5 = Position(-0.9,0.0)
    
    # print(recroomt1.tiles)
    # print(recroomt1.clean_tile_at_position(position_test1, 1))
    # print(cleanroom.tiles)
    # print(cleanroom.clean_tile_at_position(position_test1, 1))
    # print(cleanroom.tiles)
    # recroomt1.clean_tile_at_position(position_test2, 2)
    # recroomt1.clean_tile_at_position(position_test3, 1)
    # print(recroomt1.is_tile_cleaned(0, 0))
    # print(recroomt1.is_tile_cleaned(1, 2))
    # print(recroomt1.is_tile_cleaned(2, 3))
    # print(recroomt1.get_num_cleaned_tiles())
    # print(recroomt1.is_position_in_room(position_test1))
    # print(recroomt1.is_position_in_room(position_test2))
    # print(recroomt1.is_position_in_room(position_test4))
    # print(recroomt1.get_dirt_amount(2, 3))
    # print(recroomt1.get_dirt_amount(0, 0))
    
    # print(robott1)
    # print(robott1.get_robot_position())
    # print(robott1.get_robot_direction())
    # robott1.set_robot_position(position_test1)
    # print(robott1.get_robot_position())
    # robott1.set_robot_direction(275.679)
    # print(robott1.get_robot_direction())
    
    # print(eroomt1.get_num_tiles())
    # print(eroomt1.is_position_in_room(position_test1))
    # print(eroomt1.is_position_in_room(position_test4))
    # print(eroomt1.get_random_position())
    
    # froomt1.add_furniture_to_room()
    # print(froomt1.tiles)
    # print(froomt1.furniture_tiles)
    # print(froomt1.is_tile_furnished(1,1))
    # print(froomt1.is_position_furnished(position_test1))
    # print(froomt1.is_position_valid(position_test1), position_test1)
    # print(froomt1.is_position_valid(position_test2), position_test2)
    # print(froomt1.is_position_valid(position_test4), position_test4)
    # print(froomt1.get_num_tiles())
    # print(froomt1.get_random_position())
    
    # print(srobott1.update_position_and_clean())
    # print(srobott2.update_position_and_clean())
    # print(srobott3.update_position_and_clean())
    # print(srobott4.update_position_and_clean())
    
    # print(flrobott1.pos, flrobott1.angle)
    # flrobott1.update_position_and_clean()
    # print(flrobott1.pos, flrobott1.angle)
    
    # standard = run_simulation(1, 1, 1, 30, 6, 2, 0.8, 30, StandardRobot)
    # faulty = run_simulation(1, 1, 1, 30, 6, 2, 0.8, 30, FaultyRobot)
    # print('standart:', standard, 'faulty:', faulty, '% increase:', (faulty - standard)/standard*100, '%')
    
if __name__ == '__main__':
    test_work()
# print ('5x5, 100, avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('10x10, 80, avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('10x10, 90, avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('20x20, 50, avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('20x20, 50, 3r, avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
# NOTE: I WAS UNABLE TO RUN THE SIMULATION AT THE END OF THE CODE LIKE THE INSTRUCTIONS SAID. THE PYLAB WINDOW
# CRASHED. INSTEAD, I JUST RAN THE TESTS ON MY OWN AND RECORDED THE DATA
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#   The standard robot is about 20% more effecient. with 1 robot, 1 speed, 2 dirt value, and 1 capacity, 
#   the standard got 1436.9 ticks on average, while the faulty got 1746.57, or a 21.55% increase
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#   10x30: standard:1140.4, faulty:1430.27, increase of 25.42%
#   20x15: standard:1112.0, faulty:1355.37, increase of 21.89%
#   30x6: standard:729.37, faulty:980.27, increase of 34.4%
#   

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various \
#                               numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room \
#                       shapes','Aspect Ratio', 'Time / steps')
