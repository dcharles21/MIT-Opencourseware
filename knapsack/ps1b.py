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
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest
    value (1 = d1 < d2 < ... < dk)
    
    target_weight - int, amount of weight we want to find eggs to fit
    
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this
    parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """

    if (len(egg_weights), target_weight) in memo:
        result = memo[(len(egg_weights), target_weight)]


    if egg_weights == () or target_weight == 0:
        result = (0, 0)

    elif egg_weights[0] > target_weight:
        #Explore right branch only
        result = dp_make_weight(egg_weights[1:], target_weight, memo)

    else:
        nextegg = egg_weights[0]

        # Explore left branch
        Val, TakeEgg = dp_make_weight(egg_weights, target_weight - nextegg, memo)
        Val += nextegg

        # Explore right branch
        NoVal, NoEgg = dp_make_weight(egg_weights[1:], target_weight, memo)
        
        # Choose better branch
        if Val > NoVal:
            result = (Val, TakeEgg + 1)   

        elif Val == NoVal:

            if TakeEgg + 1 <= NoEgg:
                result = (Val, TakeEgg + 1)

            else:
                result = (NoVal, NoEgg)
    
        else:
            result = (NoVal, NoEgg)

    memo[(len(egg_weights), target_weight)] = result 
    return result

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n)[1])
    print()
