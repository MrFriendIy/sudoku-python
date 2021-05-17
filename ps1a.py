###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1




def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}
    file = open(filename, 'r')
    for line in file:
            cow_dict[str.split(line, ',')[0]] = int(str.split(line, ',')[1])
    return(cow_dict)
        
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips = [[]]
    # repeat until there are no more cows
    while cows != {}:
        temp_limit = limit
        temp_cows = cows.copy()
        # check to see if the heaviest cow can fit
        while True:
            heaviest = ['',0]
            for c in temp_cows:
                if int(temp_cows[c]) > heaviest[1]:
                    heaviest[0] = c
                    heaviest[1] = int(temp_cows[c])
            if temp_limit - heaviest[1] >=0:
                # if it can, add it to the current trip
                temp_limit -= heaviest[1]
                trips[-1].append(heaviest[0])
                del temp_cows[heaviest[0]]
                del cows[heaviest[0]]
            # if it cannot, try the next heaviest
            elif temp_limit - heaviest[1] < 0:
                del temp_cows[heaviest[0]]
            # once there are no more cows that can fit, create a new trip
            if cows == {}:
                break
            if temp_cows == {}:
                trips.append([])
                break
    return(trips)
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # search through all the partitions of cows
    smallest_trip = []
    for i in range(limit):
        smallest_trip.append(i)
    for part in get_partitions(cows):
        too_heavy = False
        for trip in part:
            weight_count = 0
            # add up the combined weight of the cows in each trip
            for cow in trip:
                weight_count += cows[cow]
                if weight_count > limit:
                    too_heavy = True
        # if the weight of the trip is not too much, see if its length is smaller than the current smallest
        if not too_heavy:
            if len(part) < len(smallest_trip):
                smallest_trip = part
        # once you have gone though all the sets, return the smallest
    return(smallest_trip)
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start_greedy = time.time()
    print('greedy length:', len(greedy_cow_transport(load_cows('ps1_cow_data.txt'))))
    end_greedy = time.time()
    print('greedy_time:', end_greedy - start_greedy)
    start_brute = time.time()
    print('brute length:', len(brute_force_cow_transport(load_cows('ps1_cow_data.txt'))))
    end_brute = time.time()
    print('brute time:', end_brute - start_brute)
    
