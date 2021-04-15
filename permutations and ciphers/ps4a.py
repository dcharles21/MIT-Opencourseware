# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def Insert(letter, p_list):

    '''
    Takes a letter and list of permutations 
    
    returns a list of permutations for all characters
    '''

    L1 = []

    for i in p_list:
        for j in range(0, len(i) + 1):

            L2 = list(i)  
            L2.insert(j, letter)

            L1.append(''.join(L2))

    return L1

def get_permutations(s):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
           
    if len(s) == 1:
        return list(s)

    else:        
        return Insert(s[0], get_permutations(s[1:]))

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    
    print(get_permutations('abc'))
