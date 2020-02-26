import math
import random

length = 17
num_tries = 10  # number of tries to repeat Exch to get diff result
num_tries_index = 10  # number of tries to repeat Exch to get diff result
zero_index = {}  # map from car number to index start. dummy car starts at Ncars+1


def main():
    init = [1, 1, 0, 2, 2, 3, 3, 0, 4, 4, 5, 5, 0, 6, 6, 7, 7]
    new = oneReinsert(init, 3, 7)
    print(init)
    print(new)


def twoExch(old_solution, nCars):
    """
    swap two random numbers within one random car
    can return same solution
    ! never swaps call between cars
    maintains validity
    :type old_solution: list
    :return: new solution
    """
    for x in range(num_tries):
        solution = old_solution.copy()
        carNumber = math.ceil(random.random() * nCars)
        start, stop = get_car_index(carNumber, solution, nCars)
        if start == stop + 1 or start == stop - 1:
            # empty car or two calls in car
            if x == num_tries - 1:
                return solution
            continue
        break
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    for i in range(num_tries_index):
        if solution[t1] != solution[t2]:
            continue
        else:
            t2 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    assert solution[t1] != 0 and solution[t2] != 0
    #print("swapped ", solution[t1], solution[t2])
    return solution


def threeExch(old_solution, nCars):
    """
     swap three random numbers within one random car
     can return same solution
     ! never swaps call between cars
     maintains validity
     :return: new solution
     """
    for x in range(num_tries):
        solution = old_solution.copy()
        carNumber = math.ceil(random.random() * nCars)
        start, stop = get_car_index(carNumber, solution, nCars)
        if start == stop + 1 or start == stop - 1:
            # empty car or two calls in car
            if x == num_tries - 1:
                #print("gives up, return same solution")
                return solution
            continue
        break
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    t3 = random.randint(start, stop)
    for i in range(num_tries_index*2):
        if t1 != t2 and t2 != t3 and t1 != t3:
            continue
        else:
            t2 = random.randint(start, stop)
            t3 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = solution[t3]
    solution[t3] = temp

    assert solution[t1] != 0 and solution[t2] != 0 and solution[t3] != 0
    # if solution == old_solution:
    # print("swapped", solution[t1], solution[t2], solution[t3])
    return solution


def oneReinsert(initSolution: list, nCars, nCalls):
    """
    swap a random call to new random car
    """
    solution = initSolution.copy()
    call = math.ceil(nCalls * random.random())
    # remove call from first car(all cars)
    assert call in solution #, ("".join(solution) +" - " + str(call))
    solution.remove(call)
    solution.remove(call)
    # add randomly to new car
    carNumber = math.ceil(random.random() * (nCars + 1))
    start, stop = get_car_index(carNumber, solution, nCars)
    if start == stop + 1:
        # empty car
        solution.insert(start, call)
        solution.insert(start, call)
    else:
        t1 = random.randint(start, stop)
        t2 = random.randint(start, stop)
        solution.insert(t1, call)
        solution.insert(t2, call)
    # print("inserted ", call, "at ", carNumber)
    # update indexes
    assert call != 0
    return solution
    

def get_car_index(carNumber, solution, nCars):
    carIndex = 1
    found = False
    for n, i in enumerate(solution):
        if carIndex == carNumber and not found:
            start = n
            found = True
            if carNumber == nCars + 1:
                # there is no stop 0
                stop = len(solution)
        if i == 0:
            carIndex += 1
        if carIndex == carNumber + 1:
            stop = n - 1
            break
    # TODO: can throw start referenced before assignment
    return start, stop

def threeExchRandom(oldSolution, nCars):
    solution = oldSolution.copy()
    t1 = random.randint(0, len(solution) - 1)
    t2 = random.randint(0, len(solution) - 1)
    t3 = random.randint(0, len(solution) - 1)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = solution[t3]
    solution[t3] = temp
    return solution


def twoExchRandom(oldSolution, nCars):
    solution = oldSolution.copy()
    t1 = random.randint(0, len(solution) - 1)
    t2 = random.randint(0, len(solution) - 1)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    return solution


if __name__ == '__main__':
    main()


def twoExchFast(oldSolution, nCars):
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
    start = zero_index[carNumber]
    stop = zero_index[carNumber + 1] - 2
    if start == stop + 1:
        # empty car
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    assert solution[t1] != 0, (t1, t2)
    assert solution[t2] != 0, (t1, t2)
    for i in range(5):
        if solution[t1] != solution[t2]:
            continue
        else:
            t2 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    return solution


def threeExchFast(old_solution, nCars):
    """
     swap three random numbers within one random car
     can return same solution
     ! never swaps call between cars
     maintains validity
     :return: new solution
     """
    solution = old_solution.copy()
    carNumber = math.ceil(random.random() * nCars)
    start = zero_index[carNumber]
    stop = zero_index[carNumber + 1] - 2
    if start == stop + 1:
        return solution
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    t3 = random.randint(start, stop)
    for i in range(3):
        if solution[t1] != solution[t2] and solution[t2] != solution[t3]:
            continue
        else:
            t2 = random.randint(start, stop)
            t3 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = solution[t3]
    solution[t3] = temp
    assert solution[t1] != 0 and solution[t2] != 0 and solution[t3] != 0
    if solution == old_solution:
        print("swapped", solution[t1], solution[t2], solution[t3])
    return solution
