class Feasibility:

    def __init__(self, data):
        self.data=data

    def get_car_index(self, carNumber, solution, nCars):
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

    def is_feasible_car(self, solution, carN):
        vehicleDict = self.data.getVehiclesDict()
        vertexDict = self.data.getVertexDict()
        callsDict = self.data.getCallsDict()
        nodeDict = self.data.getNodes()
        home, curTime, cap = vehicleDict[1]
        curNode = home
        carIndex = carN
        curWeight = 0
        maxWeight = cap
        startedCalls = []

        for call in solution:
            if call == 0:
                carIndex = carIndex + 1
                if carIndex >= self.data.num_vehicles + 1:
                    # dummy car
                    return True
                startedCalls = []
                curWeight = 0
                curNode, curTime, maxWeight = vehicleDict[carIndex]
                continue

            (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
            firstVisit = call not in startedCalls
            #compitable check
            if not self.data.isCompatible(carIndex, call):
                return False
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

    def is_feasible(self, solution):
        return self.onlyPairs(solution) and self.sizeTimeLimit(solution)


    def sizeTimeLimit(self, solution):
        vehicleDict = self.data.getVehiclesDict()
        vertexDict = self.data.getVertexDict()
        callsDict = self.data.getCallsDict()
        nodeDict = self.data.getNodes()
        home, curTime, cap = vehicleDict[1]
        curNode = home
        carIndex = 1
        curWeight = 0
        maxWeight = cap
        startedCalls = []

        for call in solution:
            if call == 0:
                carIndex = carIndex + 1
                if carIndex >= self.data.num_vehicles + 1:
                    # dummy car
                    return True
                startedCalls = []
                curWeight = 0
                curNode, curTime, maxWeight = vehicleDict[carIndex]
                continue

            (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
            firstVisit = call not in startedCalls
            #compitable check
            if not self.data.isCompatible(carIndex, call):
                return False
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



    def onlyPairs(self, solution):
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