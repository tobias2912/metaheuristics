from reader import Reader
# solution
carCalls = []
reader = Reader()
freeCalls = []


def main():
    print("starting")
    reader.readfile("Call_7_Vehicle_3.txt")
    carCalls = generateSolution()
    print(carCalls)
    if isFeasible(carCalls):
        print("feasible")


def isFeasible(solution):
    return onlyPairs(solution) and sizeLimit(solution)


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
        count[call] = count[call]+1
    for c in count.keys():
        if count[c] != 2:
            print("call", c, "found ", count[c], "times")
            return False
    return True


def sizeLimit(solution):
    carIndex = 1
    curWeight = 0
    visited = []
    vehicleDict=reader.getVehiclesDict()
    for call in solution:
        if call == 0:
            carIndex = carIndex+1
            visited = []
            curWeight = 0
            continue
        #print(carIndex, reader.num_vehicles)
        if carIndex==reader.num_vehicles:
            #dummy car
            return True
        if call not in visited:
            #load and check
            visited.append(call)
            curWeight = curWeight+reader.callWeight(call)
            _, _, cap = vehicleDict[carIndex]
            if curWeight >cap:
                return False
        else:
            #unload
            visited.remove(call)
            curWeight = curWeight-reader.callWeight(call)
    return True


def generateSolution():
    carCalls = []
    freeCalls = list(range(1, reader.getNumCalls()+1))
    for carN, home, start, cap in reader.getVehicles():
        # car n does all possible calls
        currentTime = start
        currentNode = home
        currentCapacity = 0
        for callN, origin, dest, size, cost, lowerPickup, upperPickup, lowerDel, upperDel in reader.getCalls():
            if reader.isCompatible(carN, callN) and callN in freeCalls and currentCapacity+size <= cap:
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
