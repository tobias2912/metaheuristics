import math
import random

from feasibility import Feasibility
from src.reader import Reader

length = 17
num_tries = 10  # number of tries to repeat Exch to get diff result
num_tries_index = 10  # number of tries to repeat Exch to get diff result
zero_index = {}  # map from car number to index start. dummy car starts at Ncars+1


def main():
    init = [1, 1, 0, 2, 2, 3, 3, 0, 4, 4, 5, 5, 6, 6, 7, 7, 0]
    print(init)


"""
all operators in format op(incumbent, data, feasibel
"""



def similar_two_exchange(solution, data, feasibel):
    """
    in random nen empty car, select node and swap with similar
    """
    start, stop, car_number = get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    # choose random index i1, call c1
    i1 = random.randint(start, stop)
    c1 = solution[i1]
    best_match_index = start
    # find most similar index
    for index, call in enumerate(solution[start: stop + 1]):
        if call == c1:
            continue
        if
    best_solution = solution.copy()
    best_cost = 0
    for t2 in solution[start: stop + 1]:
        if i1 == t2:
            continue
        new_solution = solution.copy()
        temp = new_solution[i1]
        new_solution[i1] = new_solution[t2]
        new_solution[t2] = temp
        if feasibel.is_feasible(new_solution):
            new_cost = feasibel.total_cost(new_solution)
            if new_cost < best_cost:
                best_cost = new_cost
                best_solution = new_solution
    return best_solution


def __similarity(call1, call2):


def cluster_operator():
    pass


def greedy_two_exchange(solution, data: Reader, feasibel: Feasibility):
    """
    in random non empty car, take most costly node and move to best objective solution
    """
    # choose random non-empty car
    start, stop, car_number = get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    t1 = most_expensive_node(solution, data, car_number)
    best_solution = solution.copy()
    best_cost = 0
    for t2 in solution[start: stop + 1]:
        if t1 == t2:
            continue
        new_solution = solution.copy()
        temp = new_solution[t1]
        new_solution[t1] = new_solution[t2]
        new_solution[t2] = temp
        if feasibel.is_feasible(new_solution):
            new_cost = feasibel.total_cost(new_solution)
            if new_cost < best_cost:
                best_cost = new_cost
                best_solution = new_solution
    return best_solution


def most_expensive_node(solution, data: Reader, car_number):
    """
    cost of node evenly based on time spent and money

    Returns:
        index of node
    """
    start, stop, is_empty = get_nonempty_car(solution, data)
    nodes = data.getNodes()
    visited_calls = []
    best_index, best_cost = 0, 0
    if is_empty:
        return start
    for index, call in enumerate(solution[start: stop + 1]):
        origintime, origincosts, destinationtime, destinationcosts = nodes[car_number, call]
        if call in visited_calls:
            cost = destinationtime + destinationcosts / 1000
        else:
            cost = origintime + origincosts / 1000
        if cost > best_cost:
            best_index = index
    return best_index


def get_nonempty_car(solution, data: Reader):
    """
    try to get nonempty car
    an return None car

    Returns:
        tuple: (start, stop, car_number)
    """
    for i in range(num_tries):
        car_number = math.ceil(random.random() * (data.num_vehicles + 1))
        start, stop = get_car_index(car_number, solution, data.num_vehicles)
        if start != stop + 1:
            return start, stop, car_number
    return start, stop, None


def greedy_one_reinsert(init_solution, data: Reader, feasibel):
    """
    swap a random call to new random car
    insert into best objective value
    """

    solution = init_solution.copy()
    call = math.ceil(data.num_calls * random.random())
    # remove call from first car(all cars)
    assert call in solution, ("".join(solution) + " - " + str(call))
    solution.remove(call)
    solution.remove(call)
    # add randomly to new car
    car_number = math.ceil(random.random() * (data.num_vehicles + 1))
    start, stop = get_car_index(car_number, solution, data.num_vehicles)
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


def two_exch(old_solution, data, feasibel):
    """
    swap two random numbers within one random car
    can return same solution
    ! never swaps call between cars
    maintains validity
    :type old_solution: list
    :return: new solution
    """
    n_cars = data.num_vehicles
    for x in range(num_tries):
        solution = old_solution.copy()
        car_number = math.ceil(random.random() * n_cars)
        start, stop = get_car_index(car_number, solution, n_cars)
        if start == stop + 1 or start == stop - 1:
            # empty car or two calls in car
            if x == num_tries - 1:
                return solution
            continue
        break
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    for _ in range(num_tries_index):
        if solution[t1] != solution[t2]:
            continue
        else:
            t2 = random.randint(start, stop)
    temp = solution[t1]
    solution[t1] = solution[t2]
    solution[t2] = temp
    assert solution[t1] != 0 and solution[t2] != 0
    # print("swapped ", solution[t1], solution[t2])
    return solution


def threeExch(old_solution, data, feasible):
    """
     swap three random numbers within one random car
     can return same solution
     ! never swaps call between cars
     maintains validity
     :return: new solution
     """
    n_cars = data.num_vehicles
    for x in range(num_tries):
        solution = old_solution.copy()
        carNumber = math.ceil(random.random() * n_cars)
        start, stop = get_car_index(carNumber, solution, n_cars)
        if start == stop + 1 or start == stop - 1:
            # empty car or two calls in car
            if x == num_tries - 1:
                # print("gives up, return same solution")
                return solution
            continue
        break
    t1 = random.randint(start, stop)
    t2 = random.randint(start, stop)
    t3 = random.randint(start, stop)
    for _ in range(num_tries_index * 2):
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


def one_reinsert(init_solution: list, data: Reader, feasible):
    """
    swap a random call to new random car
    """
    n_calls = data.num_calls
    n_cars = data.num_vehicles
    solution = init_solution.copy()
    call = math.ceil(n_calls * random.random())
    # remove call from first car(all cars)
    assert call in solution  # , ("".join(solution) +" - " + str(call))
    solution.remove(call)
    solution.remove(call)
    # add randomly to new car
    carNumber = math.ceil(random.random() * (n_cars + 1))
    start, stop = get_car_index(carNumber, solution, n_cars)
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


def get_car_index(car_number, solution, num_cars):
    """
    all call indices start <= i <= stop are part of car
    """
    carIndex = 1
    found = False
    for n, i in enumerate(solution):
        if carIndex == car_number and not found:
            start = n
            found = True
            if car_number == num_cars + 1:
                # there is no stop 0
                stop = len(solution)
        if i == 0:
            carIndex += 1
        if carIndex == car_number + 1:
            stop = n - 1
            break
    # TODO: can throw start referenced before assignment
    return start, stop


if __name__ == '__main__':
    main()
