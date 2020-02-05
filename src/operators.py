import math
import random

length = 17


def twoExch(solution, nCars):
    """
    swap two random numbers within one random car
    can return same solution
    ! never swaps call between cars
    maintains validity
    :type solution: list
    :return: new solution
    """
    assert len(solution) == length
    solution = solution.copy()
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
            stop = n - 1
            break
    if start == stop + 1:
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    assert len(solution) == length
    assert solution[t1] != 0 and solution[t2] != 0
    return solution


def threeExch(solution, nCars):
    """
     swap three random numbers within one random car
     can return same solution
     ! never swaps call between cars
     maintains validity
     :return: new solution
     """
    assert len(solution) == length
    solution = solution.copy()
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
            stop = n - 1
            break
    if start == stop + 1:
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    t3 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = solution[t3]
    solution[t3] = temp
    assert solution[t1] != 0 and solution[t2] != 0 and solution[t3] != 0
    assert len(solution) == length
    return solution


def oneReinsert(initSolution: list, nCars, nCalls):
    """
    swap a random call to new random car
    :param solution:
    """
    solution = initSolution.copy()
    call = math.ceil(nCalls * random.random())
    # remove call from first car(all cars)
    assert call in solution
    solution.remove(call)
    solution.remove(call)
    # add randomly to new car
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
            stop = n - 1
            break
    if start == stop + 1:
        # empty car
        solution.insert(start, call)
        solution.insert(start, call)
    else:
        t1 = random.randint(start, stop)
        t2 = random.randint(start, stop)
        solution.insert(t1, call)
        solution.insert(t2, call)
    # print("inserted ",call, "at ",carNumber)
    assert call != 0
    return solution


print(oneReinsert([0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], 3, 7))
