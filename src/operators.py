import math
import random

length = 17


def main():
    init = [1, 1, 0, 2, 2, 3, 3, 0, 4, 4, 5, 5, 0, 6, 6, 7, 7]
    new = oneReinsert(init, 3, 7)
    print(init)
    print(new)


def twoExch(oldSolution, nCars):
    """
    swap two random numbers within one random car
    can return same solution
    ! never swaps call between cars
    maintains validity
    :type oldSolution: list
    :return: new solution
    """
    solution = oldSolution.copy()
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
        #print("stop")
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    #print("swaps", t1, t2)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    assert solution[t1] != 0 and solution[t2] != 0
    return solution


def threeExch(oldsolution, nCars):
    """
     swap three random numbers within one random car
     can return same solution
     ! never swaps call between cars
     maintains validity
     :return: new solution
     """
    solution = oldsolution.copy()
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
    #print("swapped", t1, t2, t3)
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
    carNumber = math.ceil(random.random() * (nCars+1))
    carIndex = 1
    found = False
    for n, i in enumerate(solution):
        if carIndex == carNumber and not found:
            start = n
            found = True
            if carNumber == nCars+1:
                # there is no stop 0
                stop = len(solution)
        if i == 0:
            carIndex += 1
        if carIndex == carNumber + 1:
            stop = n - 1
            break
    #print("between", start, stop)
    if start == stop + 1:
        # empty car
        solution.insert(start, call)
        solution.insert(start, call)
    else:
        t1 = random.randint(start, stop)
        t2 = random.randint(start, stop)
        solution.insert(t1, call)
        solution.insert(t2, call)
    #print("inserted ", call, "at ", carNumber)
    assert call != 0
    return solution


if __name__ == '__main__':
    main()
