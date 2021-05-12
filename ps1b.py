###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1


def recursive_eggs(target_weight, eggs):
    target_weight = target_weight
    if target_weight == 0:
        return(0)
    if target_weight < 0:
        return target_weight
    smallest = target_weight
    for e in eggs:
        count = 1 + recursive_eggs(target_weight - e, eggs)
        if count < smallest:
            smallest = count
    return smallest

def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # base case if target_weight_weight == 0. return zero, as that is how many eggs you can take
    if target_weight == 0:
        return(0)
    # base case if target_weight weight < 0. return target_weight to ensure that any case with this cannot be smaller than the optimal solution
    if target_weight < 0:
        return(target_weight+egg_weights[-1])
    # define a counter varaible smallest to keep track of the smallest number of eggs so far. set it to target_weight so its initial value is always lower
    # or equal to the actual best answer
    smallest = target_weight+egg_weights[-1]
    # recursive case. loop over each of the eggs in egg weights, and create a variable count and set it equal to 
    # 1 + recursive_eggs(egg_weights, target_weight - e)
    try:
            return(memo[target_weight])
    except KeyError:
        for e in egg_weights:
            count = 1 + dp_make_weight(egg_weights, target_weight - e, memo)
            # check to see if count is smaller than smallest. if it is, set smallet = cont
            if count < smallest:
                memo[target_weight] = count
                smallest = count
    # return smallest
    return(smallest)


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()