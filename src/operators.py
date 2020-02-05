import math
import random


def twoExch(solution, nCars):
    """
    swap two random numbers within one random car
    can return same solution
    :return: new solution
    """
    carNumber = math.ceil(random.random() * nCars)
    carIndex = 1
    found = False
    for n, i in enumerate(solution):
        if carIndex == carNumber and not found:
            start = n
            found = True
        if i == 0:
            carIndex += 1
        if carIndex == carNumber + 1:
            stop = n-1
            break
    if start == stop+1:
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    assert solution[t1] != 0 and solution[t2] != 0
    return solution


print(twoExch([3, 3, 0, 1, 2, 3, 4, 5, 0, 7, 8, 9, 10, 0, 12], 3))
