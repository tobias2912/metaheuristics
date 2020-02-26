# from reader import Reader
import math
import random
import numpy as np
import time
import operators as ops
from reader import Reader

data = Reader()
files = ["data/Call_7_Vehicle_3.txt", "data/Call_18_Vehicle_5.txt", "data/Call_035_Vehicle_07.txt",
         "data/Call_080_Vehicle_20.txt", "data/Call_130_Vehicle_40.txt"]


def main():
    #data.readfile("data/Call_7_Vehicle_3.txt")  # 5M er best
    #test_annealing()
    test_all()
    #data.readfile("data/Call_035_Vehicle_07.txt")  # 5M er best



def test_annealing():
    iterations = 3
    #data.readfile("data/Call_7_Vehicle_3.txt")  # 14 er best
    data.readfile("data/Call_18_Vehicle_5.txt")  # 2,5M er best
    #data.readfile("data/Call_035_Vehicle_07.txt")  # 5M er best
    #data.readfile("data/Call_080_Vehicle_20.txt")  # 13M er best
    
    sol, best, time, best_solution = run_heuristic(annealingSetup, iterations, create_init_solution())
    print("\n\n annealing test result")
    print("avg {} best {} time {:.3}".format(round(sum(sol) / iterations), best, time))
    print(best_solution)


def run_heuristic(func, num_iterations, init_solution):
    """
    :rtype: solution, best objective, time
    """
    solution_objectives = []
    best_sol=[]
    bestTotal = total_cost(init_solution)
    start = time.time()
    for _ in range(num_iterations):
        sol, total = func(init_solution)
        if total < bestTotal:
            bestTotal = total
            best_sol=sol
        solution_objectives.append(total)
    end = time.time()
    return solution_objectives, bestTotal, end - start, best_sol


def annealingSetup(init_solution):
    iterations = 10000
    pMax = 0.9
    pMin = 0.1
    p1 = 0.05
    p2 = 0.1
    a = 0.9985
    minDelta, maxDelta = getDeltaE()
    #print("\n annealing setup")
    #print(f'min and max deltas {round(minDelta)}, {round(maxDelta)}')
    t1 = -minDelta / np.log(pMax)
    t2 = -maxDelta / np.log(pMax)
    t3 = -minDelta / np.log(pMin)
    t4 = -maxDelta / np.log(pMin)
    startTemp = max(t1, t2, t3, t4)
    endTemp = min(t1, t2, t3, t4)
    #print("starttemp", round(startTemp), "endtemp", round(endTemp), "a", a)
    solution, objective = simulatedAnnealing(init_solution, p1, p2, startTemp, a, iterations)
    return solution, objective


def simulatedAnnealing(initSolution, p1, p2, tempStart, a, iterations=10000):
    """
    :param initSolution: random solution
    :param p1: 2-exch probability
    :param p2: 3-exch proability
    :param tempStart: start temperature
    :param a: cooling
    :param iterations: default 10k
    """
    incumbent = initSolution.copy()
    bestSolution = initSolution.copy()
    temp = tempStart
    feasible_list = []
    random_accepts_list = []
    better_count_list = []
    record_list=[]
    better_count, random_accepts_count, no_changes1, no_changes2, no_changes3, feasible_count, record_count = 0,0, 0, 0, 0, 0, 0
    for i in range(iterations):
        if i % 1000 == 0:
            random_accepts_list.append(random_accepts_count)
            better_count_list.append(better_count)
            feasible_list.append(feasible_count)
            record_list.append(record_count)
            better_count, random_accepts_count, feasible_count, record_count = 0, 0, 0, 0
        #try to generate feasible solution
        rand = random.random()
        for i in range(10):
            if rand < p1:
                newSolution = ops.twoExch(incumbent, data.num_vehicles)
            elif rand < p1 + p2:
                newSolution = ops.threeExch(incumbent, data.num_vehicles)
            else:
                newSolution = ops.oneReinsert(incumbent, data.num_vehicles, data.num_calls)
            if is_feasible(newSolution):
                break
        if not is_feasible(newSolution):
            continue
        feasible_count += 1
        if newSolution == incumbent:
            if rand < p1:
                no_changes1 += 1
            elif rand < p1 + p2:
                no_changes2 += 1
            else:
                no_changes3 += 1
            continue
        deltaE = total_cost(newSolution) - total_cost(incumbent)
        if deltaE > 0:
            #print("iteration", i, "deltaE", deltaE, "temp", round(temp))
            #print("--- chance of accept is {:.1f} %".format(100*math.e ** (-deltaE / temp)))
            pass
        if deltaE < 0:
            # print("accepts better solution")
            incumbent = newSolution.copy()
            better_count += 1
            if total_cost(incumbent) < total_cost(bestSolution):
                record_count+=1
                bestSolution = incumbent.copy()
        elif random.random() < math.e ** (-deltaE / temp):
            if deltaE != 0:
                random_accepts_count += 1
            incumbent = newSolution.copy()
        temp = temp * a
    random_accepts_list.append(random_accepts_count)
    better_count_list.append(better_count)
    feasible_list.append(feasible_count)
    record_list.append(record_count)
    record_list.pop(0)
    random_accepts_list.pop(0)
    better_count_list.pop(0)
    feasible_list.pop(0)
    # print("\nannealing search results:")
    # print("temperature ended at ",temp)
    # print("best objective is ", total_cost(bestSolution))
    # print("no changes by operator:", no_changes1, no_changes2, no_changes3)
    # print("feasible, better, random, better")
    # for i in range(len(feasible_list)):
    #     print('   {:6}{:6}{:6}{:6}'.format(feasible_list[i], better_count_list[i], random_accepts_list[i], record_list[i]))
    return bestSolution, total_cost(bestSolution)


def test_all():
    num_iterations = 10
    for file in files:
        print("\n\nopening file", file,"\n\n")
        data.readfile(file)
        init_solution = create_init_solution()
        init_total = total_cost(init_solution)
        #random
        random_solutions, best_total, runtime, best_solution = run_heuristic(random_search, num_iterations, init_solution)
        print("random search avg: ", sum(random_solutions) / num_iterations, "best", best_total)
        print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        #local search
        local_solutions, best_total, runtime, best_solution = run_heuristic(local_search, num_iterations, init_solution)
        print("local search avg: ", sum(local_solutions) / num_iterations, "best", best_total)
        print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        #annealing
        annealing_solutions, best_total, runtime, best_solution = run_heuristic(annealingSetup, num_iterations, init_solution)
        print("annealing search avg: ", sum(annealing_solutions) / num_iterations, "best", best_total)
        print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        print(best_solution)


def getDeltaE():
    """
    do some reinserts to guess deltaE
    """
    diff = []
    sol = generateSolution()
    for _ in range(10):
        newsol = ops.oneReinsert(sol, data.num_vehicles, data.num_calls)
        t1 = total_cost(newsol)
        t2 = total_cost(sol)
        d = abs(t2 - t1)
        if d != 0:    
            diff.append(abs(t2 - t1))
        sol = newsol
    assert len(diff)>1, len(diff)
    return np.percentile(diff, 10), np.percentile(diff, 90)


def create_init_solution():
    solution = [0 for _ in range(data.num_vehicles)]
    solution += list(range(1, data.num_calls + 1))
    solution += list(range(1, data.num_calls + 1))
    return solution


def update_zeroindex(incumbent):
    ops.zero_index[1] = 0
    car_index = 2
    for n, call in enumerate(incumbent):
        if call == 0:
            ops.zero_index[car_index] = n + 1
            car_index += 1


def local_search(init_solution, p1=0.3, p2=0.3, iterations=10000):
    best_solution = init_solution.copy()
    for n in range(iterations):
        rand = ops.random.random()
        if rand < p1:
            current = ops.twoExch(best_solution, data.num_vehicles)
        elif rand < p1 + p2:
            current = ops.threeExch(best_solution, data.num_vehicles)
        else:
            current = ops.oneReinsert(best_solution, data.num_vehicles, data.num_calls)
        if is_feasible(current) and total_cost(current) < total_cost(best_solution):
            best_solution = current
    # print("localsearch best is ", totalCost(best_solution), " - ", best_solution)
    return best_solution, total_cost(best_solution)


def random_search(initSolution, iterations=10000):
    bestSolution = initSolution.copy()
    for i in range(iterations):
        currentSolution = generateRandom()
        if is_feasible(currentSolution) and total_cost(currentSolution) < total_cost(bestSolution):
            bestSolution = currentSolution
    # print("randomsearch best is", totalCost(bestSolution), " - ", bestSolution)
    # assert len(initSolution) == data.numCalls * 2 + data.num_vehicles
    return bestSolution, total_cost(bestSolution)


def is_feasible(solution):
    return onlyPairs(solution) and sizeTimeLimit(solution)


def total_cost(solution):
    vehicleDict = data.getVehiclesDict()
    vertexDict = data.getVertexDict()
    callsDict = data.getCallsDict()
    nodeDict = data.getNodes()
    home, _, _ = vehicleDict[1]
    curNode = home
    carIndex = 1
    startedCalls = []
    curCost = 0
    dummyCar = False

    for call in solution:
        if call == 0 or dummyCar:
            if carIndex + 1 > data.num_vehicles:
                dummyCar = True
                if call != 0 and call not in startedCalls:
                    (_, _, _, failCost, _, _, _, _) = callsDict[call]
                    curCost = curCost + failCost
                    startedCalls.append(call)
                continue
            # reset for next car
            carIndex = carIndex + 1
            startedCalls = []
            curNode, _, _ = vehicleDict[carIndex]
            continue

        (origin, dest, size, failCost, _, _, _, _) = callsDict[call]
        _, originCost, _, destCost = nodeDict[(carIndex, call)]
        if call not in startedCalls:
            startedCalls.append(call)
            curCost = curCost + originCost
            nextNode = origin
        else:
            startedCalls.remove(call)
            curCost = curCost + destCost
            nextNode = dest
        _, travelCost = vertexDict[(carIndex, curNode, nextNode)]
        curCost = curCost + travelCost
        curNode = nextNode
    return curCost


def sizeTimeLimit(solution):
    vehicleDict = data.getVehiclesDict()
    vertexDict = data.getVertexDict()
    callsDict = data.getCallsDict()
    nodeDict = data.getNodes()
    home, curTime, cap = vehicleDict[1]
    curNode = home
    carIndex = 1
    curWeight = 0
    maxWeight = cap
    startedCalls = []

    for call in solution:
        if call == 0:
            carIndex = carIndex + 1
            if carIndex >= data.num_vehicles + 1:
                # dummy car
                return True
            startedCalls = []
            curWeight = 0
            curNode, curTime, maxWeight = vehicleDict[carIndex]
            continue

        (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
        firstVisit = call not in startedCalls
        # capacity check
        if firstVisit:
            startedCalls.append(call)
            curWeight = curWeight + size
            if curWeight > maxWeight:
                return False
        else:
            startedCalls.remove(call)
            curWeight = curWeight - size
        # time check
        if firstVisit:
            nextNode = origin
        else:
            nextNode = dest
        travelTime, _ = vertexDict[(carIndex, curNode, nextNode)]
        originTime, _, destTime, _ = nodeDict[(carIndex, call)]
        curTime += travelTime
        if firstVisit:  # pickup
            if curTime < lowerPickup:
                # wait for pickup
                curTime = lowerPickup
            curTime += originTime
            if upperPickup < curTime:
                return False
        else:
            #delivery
            if curTime < lowerDelivery:
                curTime = lowerDelivery
            curTime += destTime
            if upperDelivery < curTime:
                return False
        curNode = nextNode
    return True


def onlyPairs(solution):
    count = {}
    for call in solution:
        if call == 0:
            for c in count.keys():
                if count[c] != 2:
                    # print("call", c, "found ", count[c], "times")
                    return False
            count.clear()
            continue
        if count.get(call) is None:
            count[call] = 0
        count[call] = count[call] + 1
    for c in count.keys():
        if count[c] != 2:
            # print("call", c, "found ", count[c], "times")
            return False
    return True


def generateSolution():
    """
    generate empty start solution
    """
    car_calls = []
    free_calls = list(range(1, data.getNumCalls() + 1))
    for carN, home, start, cap in data.getVehicles():
        # car n does all possible calls
        current_time = start
        current_node = home
        current_capacity = 0
        for callN, origin, dest, size, cost, lowerPickup, upperPickup, lowerDel, upperDel in data.getCalls():
            if data.isCompatible(carN, callN) and callN in free_calls and current_capacity + size <= cap:
                # time constraint
                pickuptime = current_time + \
                             data.travelTime(carN, current_node, origin)
                deliverytime = pickuptime + \
                               data.travelTime(carN, origin, dest)
                if lowerPickup <= pickuptime <= upperPickup and lowerDel <= deliverytime <= upperDel:
                    free_calls.remove(callN)
                    car_calls.append(callN)
                    car_calls.append(callN)
                    current_node = dest
                    current_time = deliverytime

        car_calls.append(0)
    # dummy car
    car_calls.extend(free_calls)
    car_calls.extend(free_calls)
    return car_calls


def generateRandom():
    car = {}
    num_vehicles = data.num_vehicles + 1
    for carN in range(1, num_vehicles + 1):
        car[carN] = []
    calls = range(1, data.getNumCalls() + 1)
    # map random car to all call pairs
    for call in calls:
        car_calls = car[math.ceil(random.random() * num_vehicles)]
        car_calls.append(call)
        car_calls.append(call)
    # shuffle order of delivery
    solution = []
    for carN in range(1, num_vehicles + 1):
        car_calls = car[carN]
        random.shuffle(car_calls)
        solution += car_calls
        solution += [0]
    solution.pop()
    return solution


if __name__ == "__main__":
    main()
