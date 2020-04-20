class Feasibility:

    def __init__(self, data):
        self.data = data


    def __get_car_index(self, car_number, solution, num_cars):
        """
            all call indices start <= i <= stop are part of car
            loop with solution[start:stop+1]
            Returns: (start, stop)
        """
        if car_number == num_cars + 1:
            # dummy car
            sol = solution.copy()
            start, stop = self.__get_car_index(1, sol[::-1], num_cars)
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


    def __is_feasible_car(self, solution, carN):
        """
        faster feasibility check
        only check for changes in car carN
        not working
        """
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
                if carIndex >= self.data.num_cars + 1:
                    # dummy car
                    return True
                startedCalls = []
                curWeight = 0
                curNode, curTime, maxWeight = vehicleDict[carIndex]
                continue

            (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
            firstVisit = call not in startedCalls
            # compitable check
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
                # delivery
                if curTime < lowerDelivery:
                    curTime = lowerDelivery
                curTime += destTime
                if upperDelivery < curTime:
                    return False
            curNode = nextNode
        return True

    def is_feasible(self, solution):
        return self.__onlyPairs(solution) and self.__sizeTimeLimit(solution)

    def __sizeTimeLimit(self, solution):
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
                if carIndex >= self.data.num_cars + 1:
                    # dummy car
                    return True
                startedCalls = []
                curWeight = 0
                curNode, curTime, maxWeight = vehicleDict[carIndex]
                continue

            (origin, dest, size, _, lowerPickup, upperPickup, lowerDelivery, upperDelivery) = callsDict[call]
            firstVisit = call not in startedCalls
            # compitable check
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
                # delivery
                if curTime < lowerDelivery:
                    curTime = lowerDelivery
                curTime += destTime
                if upperDelivery < curTime:
                    return False
            curNode = nextNode
        return True

    def __onlyPairs(self, solution):
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

    def total_cost(self, solution):
        vehicleDict = self.data.getVehiclesDict()
        vertexDict = self.data.getVertexDict()
        callsDict = self.data.getCallsDict()
        nodeDict = self.data.getNodes()
        home, _, _ = vehicleDict[1]
        curNode = home
        carIndex = 1
        startedCalls = []
        curCost = 0
        dummyCar = False

        for call in solution:
            if call == 0 or dummyCar:
                if carIndex + 1 > self.data.num_cars:
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

            (origin, dest, _, failCost, _, _, _, _) = callsDict[call]
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
