# from reader import Reader
import math
import random

import numpy as np
import time
import src.operators as ops
from src.reader import Reader

data = Reader()


def main():
    print("starting")
    data.readfile("data/Call_7_Vehicle_3.txt")
    # reader.readfile("data/Call_18_Vehicle_5.txt")
    # annealingSetup()
    testHeuristic()


def testHeuristic(runs=10):
    start = time.time()
    totals = []
    for i in range(runs):
        sol, cost = annealingSetup()
        totals.append(cost)
    end = time.time()
    print("average:")
    print(sum(totals) / len(totals))
    print("best:")
    print(min(totals))
    print("time used", end - start)


def annealingSetup():
    pMax = 0.8
    pMin = 0.1
    p1 = 0.2
    p2 = 0.2
    a = 0.99
    minDelta, maxDelta = getDeltaE()
    print(f'min and max deltas {round(minDelta)}, {round(maxDelta)}')
    t1 = -minDelta / np.log(pMax)
    t2 = -maxDelta / np.log(pMax)
    t3 = -minDelta / np.log(pMin)
    t4 = -maxDelta / np.log(pMin)
    startTemp = max(t1, t2, t3, t4)
    endTemp = min(t1, t2, t3, t4)
    print("starttemp", round(startTemp), "endtemp", round(endTemp))

    solution = simulatedAnnealing([0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], p1, p2, startTemp, a,
                                  iterations=10000)
    return solution


def getDeltaE():
    diff = []
    for i in range(100):
        t1 = totalCost(generateRandom())
        t2 = totalCost(generateRandom())
        diff.append(abs(t1 - t2))
    return np.percentile(diff, 30), np.percentile(diff, 70)
    return min(diff), max(diff)


def simulatedAnnealing(initSolution, p1, p2, tempStart, a, iterations=10000):
    """
    :param initSolution: random solution
    :param p1: 2-exch probability
    :param p2: 3-exch proability
    :param tempStart: start temperature (0.8)
    :param a: cooling
    :param iterations: default 10k
    """
    print("starts simulated annealing with ", initSolution,
          " p1:", p1, " p2:", p2, " start temp:", tempStart, " a:", a, " i:", iterations)
    incumbent = initSolution.copy()
    bestSolution = initSolution.copy()
    temp = tempStart
    failed = 0
    betterCount = 0
    randomAccepts = 0
    for i in range(iterations):
        print("------start iteration", i, "------")
        rand = random.random()
        if rand < p1:
            newSolution = ops.twoExch(incumbent, data.num_vehicles)
        elif rand < p1 + p2:
            newSolution = ops.threeExch(incumbent, data.num_vehicles)
        else:
            newSolution = ops.oneReinsert(incumbent, data.num_vehicles, data.numCalls)
        if not isFeasible(newSolution):
            failed += 1
            # print("failed")
            continue
        if newSolution == incumbent:
            # print("no changes")
            continue
        totnew = totalCost(newSolution)
        totinc = totalCost(incumbent)
        if totinc == totnew:
            # print("no value changes")
            continue
        # print(newSolution)
        # print(incumbent)
        print(totnew, totinc)
        deltaE = totnew - totinc
        print("deltaE", deltaE, "temp", temp)
        if deltaE > 0:
            print("chance of accepting worse is", math.e ** (-deltaE / temp))
        if deltaE < 0:
            print("accepts better solution")
            # always accept better solution
            incumbent = newSolution.copy()
            betterCount += 1
            if totalCost(incumbent) < totalCost(bestSolution):
                bestSolution = incumbent.copy()
        elif random.random() < math.e ** (-deltaE / temp):
            print("accepted worse solution")
            incumbent = newSolution.copy()
            randomAccepts += 1
        temp = temp * a
    print("\n annealing search best is ", totalCost(bestSolution), " - ", bestSolution)
    print("infeasible", failed, " random accepts", randomAccepts, "better neighbors", betterCount)
    return bestSolution, totalCost(bestSolution)


def localSearch(initSolution, p1, p2, iterations=10000):
    bestSolution = initSolution
    for n in range(iterations):
        rand = ops.random.random()
        if rand < p1 or True:
            current = ops.twoExch(bestSolution, data.num_vehicles)
        elif rand < p1 + p2:
            current = ops.threeExch(bestSolution)
        else:
            current = ops.oneReinsert(bestSolution)
        if isFeasible(current) and totalCost(current) < totalCost(bestSolution):
            bestSolution = current
    print("localsearch best is ", totalCost(bestSolution), " - ", bestSolution)
    return bestSolution


def randomSearch(initSolution, iterations=10000):
    bestSolution = initSolution
    for i in range(iterations):
        currentSolution = generateRandom()
        if isFeasible(currentSolution) and totalCost(currentSolution) < totalCost(bestSolution):
            bestSolution = currentSolution
    print("randomsearch best is", totalCost(bestSolution), " - ", bestSolution)
    assert len(initSolution) == data.numCalls * 2 + data.num_vehicles
    return bestSolution


def isFeasible(solution):
    return onlyPairs(solution) and sizeTimeLimit(solution)


def totalCost(solution):
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
        arrivalTime = curTime + travelTime
        if firstVisit:  # pickup
            if arrivalTime < lowerPickup:
                # wait for pickup
                arrivalTime = lowerPickup
            if upperPickup < arrivalTime:
                return False
            curTime = arrivalTime + originTime
        else:
            if arrivalTime < lowerDelivery:
                arrivalTime = lowerDelivery
            if upperDelivery < arrivalTime:
                return False
            curTime = arrivalTime + destTime
        curNode = nextNode
    return True


def onlyPairs(solution):
    count = {}
    for call in solution:
        if call == 0:
            for c in count.keys():
                if count[c] != 2:
                    print("call", c, "found ", count[c], "times")
                    return False
            count.clear()
            continue
        if count.get(call) is None:
            count[call] = 0
        count[call] = count[call] + 1
    for c in count.keys():
        if count[c] != 2:
            print("call", c, "found ", count[c], "times")
            return False
    return True


def generateSolution():
    carCalls = []
    freeCalls = list(range(1, data.getNumCalls() + 1))
    for carN, home, start, cap in data.getVehicles():
        # car n does all possible calls
        currentTime = start
        currentNode = home
        currentCapacity = 0
        for callN, origin, dest, size, cost, lowerPickup, upperPickup, lowerDel, upperDel in data.getCalls():
            if data.isCompatible(carN, callN) and callN in freeCalls and currentCapacity + size <= cap:
                # time constraint
                pickuptime = currentTime + \
                             data.travelTime(carN, currentNode, origin)
                deliverytime = pickuptime + \
                               data.travelTime(carN, origin, dest)
                if lowerPickup <= pickuptime <= upperPickup and lowerDel <= deliverytime <= upperDel:
                    freeCalls.remove(callN)
                    carCalls.append(callN)
                    carCalls.append(callN)
                    currentNode = dest
                    currentTime = deliverytime

        carCalls.append(0)
    # dummy car
    carCalls.extend(freeCalls)
    carCalls.extend(freeCalls)
    return carCalls


def generateRandom():
    car = {}
    n = data.num_vehicles + 1
    for carN in range(1, n + 1):
        car[carN] = []
    calls = range(1, data.getNumCalls() + 1)
    # map random car to all call pairs
    for call in calls:
        carCalls = car[math.ceil(random.random() * n)]
        carCalls.append(call)
        carCalls.append(call)
    # shuffle order of delivery
    solution = []
    for carN in range(1, n + 1):
        carCalls = car[carN]
        random.shuffle(carCalls)
        solution += carCalls
        solution += [0]
    solution.pop()
    return solution


if __name__ == "__main__":
    main()
