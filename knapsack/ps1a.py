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

    dict = {}

    f = open(filename, "r")
    
    for line in f:
        cow_data = line.split(',')
        dict[cow_data[0]] = int(cow_data[1])

    f.close()

    return dict

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

    all_trips = []    

    cows = cows.copy()
    cows_list = sorted(cows.keys(), key = cows.get)
    cows_list.reverse()

    while len(cows_list) > 0:
        
        trip = []
        weight = 0

        for i in cows_list:
            
            if weight + cows[i] <= limit:
                trip.append(i)
                weight += cows[i]            

        for i in trip:
            cows_list.remove(i)

        all_trips.append(trip)  

    return all_trips

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

    cows = cows.copy()

    result = []
    part = []
    weight = 0

    for partition in get_partitions(cows):
        part.append(partition)         


    for L in part:

        for l in L:

            weight = 0
            check = None

            for cow in l:
                weight += cows[cow]

                if weight > limit:
                    check = False

            if check == False:
                break

            if l == L[-1]:
                check = True

        if check == True:
            result = L
            break          

    return result
        
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
    # TODO: Your code here
    pass

if __name__ == "__main__":

    cows = load_cows("ps1_cow_data.txt")
    greedy_cow_transport(cows,limit=10)
    brute_force_cow_transport(cows, limit = 10)

