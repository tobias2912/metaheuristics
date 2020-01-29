# from reader import Reader
from src.reader import Reader

# solution
reader = Reader()


def main():
    print("starting")
    #reader.readfile("data/Call_7_Vehicle_3.txt")
    reader.readfile("data/Call_18_Vehicle_5.txt")
    carCalls = generateSolution()
    print(carCalls)
    if isFeasible(carCalls):
        print("feasible")
    print("objective function", totalCost(solution=carCalls))


def isFeasible(solution):
    return onlyPairs(solution) and sizeTimeLimit(solution)


def totalCost(solution):
    vehicleDict = reader.getVehiclesDict()
    vertexDict = reader.getVertexDict()
    callsDict = reader.getCallsDict()
    nodeDict = reader.getNodes()
    home, _, _ = vehicleDict[1]
    curNode = home
    carIndex = 1
    startedCalls = []
    curCost = 0
    dummyCar = False

    for call in solution:
        if call == 0 or dummyCar:
            if carIndex + 1 > reader.num_vehicles:
                dummyCar = True
                if call != 0:
                    (_, _, _, failCost, _, _, _, _) = callsDict[call]
                    curCost = curCost + failCost
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
        curNode = nextNode
    return curCost


def sizeTimeLimit(solution):
    vehicleDict = reader.getVehiclesDict()
    vertexDict = reader.getVertexDict()
    callsDict = reader.getCallsDict()
    nodeDict = reader.getNodes()
    home, curTime, cap = vehicleDict[1]
    curNode = home
    carIndex = 1
    curWeight = 0
    maxWeight = cap
    startedCalls = []

    for call in solution:
        if call == 0:
            carIndex = carIndex + 1
            startedCalls = []
            curWeight = 0
            curNode, curTime, maxWeight = vehicleDict[carIndex]
            continue
        if carIndex == reader.num_vehicles:
            # dummy car
            return True
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
    freeCalls = list(range(1, reader.getNumCalls() + 1))
    for carN, home, start, cap in reader.getVehicles():
        # car n does all possible calls
        currentTime = start
        currentNode = home
        currentCapacity = 0
        for callN, origin, dest, size, cost, lowerPickup, upperPickup, lowerDel, upperDel in reader.getCalls():
            if reader.isCompatible(carN, callN) and callN in freeCalls and currentCapacity + size <= cap:
                # time constraint
                pickuptime = currentTime + \
                             reader.travelTime(carN, currentNode, origin)
                deliverytime = pickuptime + \
                               reader.travelTime(carN, origin, dest)
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


if __name__ == "__main__":
    main()
