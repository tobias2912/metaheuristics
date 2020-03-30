import math
import random
from os import error

from feasibility import Feasibility
from src.reader import Reader

length = 17
num_tries = 10  # number of tries to repeat Exch to get diff result
num_tries_index = 10  # number of tries to repeat Exch to get diff result
zero_index = {}  # map from car number to index start. dummy car starts at Ncars+1


def main():
    init = [0, 2, 2, 0, 0, 4, 4, 5, 5, 0]
    start, stop = (__get_car_index2(init, 1, 4))


"""
all operators in format op(incumbent, data, feasibel
"""


def similar_two_exchange(solution, data, feasibel):
    """
    in random nen empty car, select node and swap with similar
    """
    start, stop, car_number = __get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    # choose random index i1, call random_call
    i1 = random.randint(start, stop - 1)
    random_call = solution[i1]
    best_match_index = start
    similiar_record = 0
    # find most similar index
    for index, call in enumerate(solution[start: stop + 1]):
        if call == random_call:
            continue
        score = __similarity_timeframe(call, random_call, data)
        if score > similiar_record:
            best_match_index = start + index
            similiar_record = score

    new_solution = solution.copy()
    temp = new_solution[i1]
    new_solution[i1] = new_solution[best_match_index]
    new_solution[best_match_index] = temp
    return new_solution


def reduce_wait_two_ex(solution, data, feasibel):
    """
    in random non empty car, select node and swap with similar
    """
    start, stop, car_number = __get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    t1 = __longest_wait_node(solution, data, feasibel, car_number)
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


def __similarity_timeframe(call1, call2, data: Reader):
    """
    similarity score of two calls based on delivery window
    if no difference, return 1
    large difference => closer to 0
    """
    calls = data.getCallsDict()
    origin1, dest1, s1, c1, lp1, up1, ld1, ud1 = calls[call1]
    origin2, dest2, s2, c2, lp2, up2, ld2, ud2 = calls[call2]
    diff = abs(lp1 - lp2) + abs(ld1 - ld2) + abs(up1 - up2) + abs(ud1 - ud2)
    if diff == 0:
        return 1
    return 1 / diff


def greedy_two_exchange(solution, data: Reader, feasibel: Feasibility):
    """
    in random non empty car, take most costly node and move to best objective solution
    """
    # choose random non-empty car
    start, stop, car_number = __get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    # t1 = most_consuming_node(solution, data, car_number)
    t1 = __most_expensive_node(solution, data)
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


def __longest_wait_node(solution, data: Reader, feasible, car_number):
    """
    longest wait node in car_number
    return index within start:stop
    """
    start, stop = __get_car_index(car_number, solution, data.num_vehicles)
    vehicleDict = data.getVehiclesDict()
    vertexDict = data.getVertexDict()
    callsDict = data.getCallsDict()
    nodeDict = data.getNodes()
    home, cur_time, cap = vehicleDict[car_number]
    cur_node = home
    car_index = car_number
    started_calls = []
    record_wait = 0
    record_index = 0
    for index, call in enumerate(solution[start: stop + 1]):
        assert call != 0
        (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
        first_visit = call not in started_calls
        if first_visit:
            started_calls.append(call)
        else:
            started_calls.remove(call)
        # time check
        if first_visit:
            next_node = origin
        else:
            next_node = dest
        travel_time, _ = vertexDict[(car_index, cur_node, next_node)]
        originTime, _, destTime, _ = nodeDict[(car_index, call)]
        cur_time += travel_time
        if first_visit:  # pickup
            if cur_time < lowerPickup:
                # wait for pickup
                wait_time = lowerPickup - cur_time
                if wait_time > record_wait:
                    record_index = index
                    record_wait = wait_time
                cur_time = lowerPickup
            cur_time += originTime
        else:
            # delivery
            if cur_time < lowerDelivery:
                # wait for pickup
                if wait_time > record_wait:
                    record_index = index
                    record_wait = wait_time
                cur_time = lowerDelivery

            cur_time += destTime
        cur_node = next_node
    return record_index


def __most_expensive_node(solution, data: Reader):
    """
        take node with highest travel and delivery cost
        Returns: index of node in solution
    """
    vehicleDict = data.getVehiclesDict()
    vertexDict = data.getVertexDict()
    callsDict = data.getCallsDict()
    nodeDict = data.getNodes()
    home, _, _ = vehicleDict[1]
    cur_node = home
    car_index = 1
    started_calls = []
    record_cost = 0
    record_index = 0
    dummy_car = False

    for index, call in enumerate(solution):
        if call == 0 or dummy_car:
            if car_index + 1 > data.num_vehicles:
                dummy_car = True
                if call != 0 and call not in started_calls:
                    (_, _, _, failCost, _, _, _, _) = callsDict[call]
                    started_calls.append(call)
                continue
            # reset for next car
            car_index = car_index + 1
            started_calls = []
            cur_node, _, _ = vehicleDict[car_index]
            continue

        (origin, dest, _, failCost, _, _, _, _) = callsDict[call]
        _, origin_cost, _, dest_cost = nodeDict[(car_index, call)]
        if call not in started_calls:
            started_calls.append(call)
            cur_cost = origin_cost
            next_node = origin
        else:
            started_calls.remove(call)
            cur_cost = dest_cost
            next_node = dest
        _, travel_cost = vertexDict[(car_index, cur_node, next_node)]
        cur_cost = cur_cost + travel_cost
        cur_node = next_node
        if cur_cost > record_cost:
            record_cost = cur_cost
            record_index = index
    return record_index


def __most_expensive_node_car(car_number, solution, data: Reader):
    """
        take node with highest travel and delivery cost in a car
        Returns: index of node in solution
    """
    vehicleDict = data.getVehiclesDict()
    vertexDict = data.getVertexDict()
    callsDict = data.getCallsDict()
    nodeDict = data.getNodes()
    home, _, _ = vehicleDict[car_number]
    cur_node = home
    car_index = car_number
    started_calls = []
    record_cost = 0
    record_index = 0
    start, stop = __get_car_index(car_number, solution, data.num_vehicles)
    for index, call in enumerate(solution[start:stop + 1]):
        (origin, dest, _, failCost, _, _, _, _) = callsDict[call]
        _, origin_cost, _, dest_cost = nodeDict[(car_index, call)]
        if call not in started_calls:
            started_calls.append(call)
            cur_cost = origin_cost
            next_node = origin
        else:
            started_calls.remove(call)
            cur_cost = dest_cost
            next_node = dest
        _, travel_cost = vertexDict[(car_index, cur_node, next_node)]
        cur_cost = cur_cost + travel_cost
        cur_node = next_node
        if cur_cost > record_cost:
            record_cost = cur_cost
            record_index = index
    return record_index


def most_consuming_node(solution, data: Reader, car_number):
    """
    cost of node evenly based on time spent and money

    Returns:
        index of node
    """
    start, stop, is_empty = __get_nonempty_car(solution, data)
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


def __get_nonempty_car(solution, data: Reader):
    """
    try to get nonempty car
    can return None car

    Returns:
        tuple: (start, stop, car_number)
    """
    for i in range(num_tries):
        car_number = math.ceil(random.random() * data.num_vehicles)
        start, stop = __get_car_index(car_number, solution, data.num_vehicles)
        if start != stop + 1:
            return start, stop, car_number
    return start, stop, None


def __get_dummy_calls(init_solution):
    """
    return list of calls with no duplicates
    """
    calls = []
    for call in reversed(init_solution):
        if call == 0:
            return calls
        if call not in calls:
            calls.append(call)
    raise error


def assign_unused_call(init_solution, data: Reader, feasible):
    """
    assign most expensive dummy call to random vehicle
    """
    # find most expensive
    init_solution = init_solution.copy()
    call_dict = data.getCallsDict()
    record_cost = 0
    record_call = None
    unused_calls = __get_dummy_calls(init_solution)
    for call in unused_calls:
        origin, dest, s, fail_cost, lp, up, ld, ud = call_dict[call]
        if fail_cost > record_cost:
            record_call = call
            record_cost = fail_cost
    call = record_call
    if call is None:
        return init_solution
    # remove call
    assert call != 0
    assert call in init_solution
    init_solution.remove(call)
    init_solution.remove(call)
    # add randomly to new car
    carNumber = math.ceil(random.random() * data.num_vehicles)
    start, stop = __get_car_index(carNumber, init_solution, data.num_vehicles)
    if start == stop + 1:
        # empty car
        init_solution.insert(start, call)
        init_solution.insert(start, call)
    else:
        t1 = random.randint(start, stop)
        t2 = random.randint(start, stop)
        init_solution.insert(t1, call)
        init_solution.insert(t2, call)
    # print("inserted ", call, "at ", carNumber)
    return init_solution


def greedy_one_reinsert(init_solution, data: Reader, feasibel: Feasibility):
    """
    in random car (not dummy), remove most expensive call. insert into best solution
    """
    solution = init_solution.copy()
    # remove call from random car
    start, stop, car_number = __get_nonempty_car(solution, data)
    if car_number is None:
        return solution
    index = __most_expensive_node_car(car_number, solution, data)
    call = solution[index]
    solution.remove(call)
    solution.remove(call)
    record_solution = None
    record_score = None
    # add call to best car
    for _ in range(num_tries):
        new_sol = solution.copy()
        car_number = math.ceil(random.random() * (data.num_vehicles + 1))
        start, stop = __get_car_index(car_number, solution, data.num_vehicles)
        if start == stop + 1:
            # empty car
            new_sol.insert(start, call)
            new_sol.insert(start, call)
        else:
            t1 = random.randint(start, stop)
            t2 = random.randint(start, stop)
            new_sol.insert(t1, call)
            new_sol.insert(t2, call)
        if feasibel.is_feasible(new_sol):
            cost = feasibel.total_cost(new_sol)
            if record_score is None or cost < record_score:
                print(new_sol)
                record_score = cost
                record_solution = new_sol
    if record_solution is not None:
        return record_solution
    else:
        return init_solution


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
        start, stop = __get_car_index(car_number, solution, n_cars)
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
        start, stop = __get_car_index(carNumber, solution, n_cars)
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
    # add randomly to new car or dummy
    carNumber = math.ceil(random.random() * (n_cars + 1))
    start, stop = __get_car_index(carNumber, solution, n_cars)
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


def __get_car_index(car_number, solution, num_cars):
    """
        all call indices start <= i <= stop are part of car
        loop with solution[start:stop+1]
        Returns: (start, stop)
    """
    if car_number == num_cars + 1:
        # dummy car
        sol = solution.copy()
        start, stop = __get_car_index(1, sol[::-1], num_cars)
        return len(solution) - stop - 1, len(solution) + 1
    # find start
    car_counter = 1
    start = 0
    for index, call in enumerate(solution):
        if call == 0:
            car_counter += 1
            if car_counter == car_number:
                start = index + 1
            if car_counter == car_number + 1:
                stop = index - 1
                return start, stop


if __name__ == '__main__':
    main()
