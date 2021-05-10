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
    file = open(filename, 'r')
    file_list = list(file)
    line_list = []
    for line in file_list:
        line = line.strip('\n')
        line_list.append(line)
        
    for i in range(len(line_list)):
        line_list[i] = str.split(line_list[i], ',')
        file_dict = {}
    for lst in line_list:
        file_dict[lst[0]] = lst[1]
    return(file_dict)
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
   # define a list "trips" with an empty list inside of it and an int called "weight_cound" = 0 and two empty lists, does and doesnt fit
    trips = [[]]
    weight_count = 0
    doesnt_fit = []
    does_fit = []
    # create a copy of the cows dict
    cows_mutable = cows.copy()
    # define a list with an empty string and an int 0 called "heaviest", search the copy cows dict for the heaviest cow that isn't in does/doesnt fit
    heaviest = ['',0]
    for cow1 in cows:
        for cow in cows_mutable:
            if int(cows_mutable[cow]) > heaviest[1] and cow not in doesnt_fit and cow not in does_fit:
                heaviest[0] = cow
                heaviest[1] = int(cows_mutable[cow])


            # check if the cow has a weight > limit - weight_count
            if heaviest[1] + weight_count - limit <= 0:

                # if it doesn't, add that cow to the last list in trips, add it weight to weight_count, append it to does_fit, and reset heaviest
                trips[len(trips)-1] += [heaviest[0]]
                does_fit.append(heaviest[0])
                weight_count += heaviest[1]
                heaviest = ['',0]

            # if the cow is too heave, append it to doesnt fit and reset heaviest
            elif heaviest[1] + weight_count - limit > 0:
                doesnt_fit.append(heaviest[0])
                heaviest = ['',0]

        # if every cow is in does or doesnt fit, set weight count to 0, remove does fit cows from cows_mutable, add an empty list to trips, reset fits
        cows_count = 1
        for cow2 in cows:
            if cow2 in does_fit or cow2 in doesnt_fit:
                # print('cows_count',cows_count, '\n len(cows_mutable)', len(cows_mutable), '\n cows', cows, '\n cows_mutable', cows_mutable,  '\n')
                cows_count += 1
            if cows_count == len(cows_mutable):
                weight_count = 0
                for c in does_fit:
                    # print('c', c, '\n', 'does_fit', does_fit, '\n', 'cows_mutable', cows_mutable, '\n', 'cows_mutable[c]', cows_mutable[c])
                    del cows_mutable[c]
                does_fit = []
                doesnt_fit = []
                if cows_mutable == {}:
                    return(trips)
                trips.append([])



    # repeat until there are no cows left
    
    
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
    # create a list of the keys in the cows dict called cows_list
    cows_list = []
    for key in cows:
        cows_list.append(key)
    
    # call get_partitions on cows_list and assign it to a new list: part_cows_list
    part_cows_list = []
    for part in get_partitions(cows_list):
        part_cows_list.append(part)

    # loop over each sublist in part_cows_list and check the wieght value of each cow in it


    for i in range(len(part_cows_list)):
        for subsublist in part_cows_list[i-1]:
            weight = 0
            for cow in subsublist:
                # add these wight values together. if it is too high, delete the list
                weight += int(cows[cow])
            if weight > limit:
                subsublist.append('remove')
    valid_trips = []    
    for lst in part_cows_list:
        bad_list = False
        for sublist in lst:
            if 'remove' in sublist:
                bad_list = True
        if not bad_list:
            valid_trips.append(lst)
            
    # after looping over every sublist, take the list with the fewest elements and return it
    smallest = valid_trips[0]
    for trip in valid_trips:
        if len(trip) < len(smallest):
            smallest = trip
    return(smallest)
        
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
    print('greedy cow transport:', len(greedy_cow_transport(load_cows('ps1_cow_data.txt'))))
    print('brute force cow transport', len(brute_force_cow_transport(load_cows('ps1_cow_data.txt'))))
    
