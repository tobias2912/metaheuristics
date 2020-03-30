class Reader:

    def __init__(self):
        self.callsDict = {}
        self.num_nodes = 0
        self.num_calls = 0
        self.num_vehicles = 0
        self.vehicles = []
        self.vehiclesDict = {}
        self.calls = []
        self.compatibleCalls = {}
        self.travel = []
        self.nodecost = {}
        self.nodeCall = {}
        self.vertex = {}

    def possibleDelivery(self, origin):
        """
        list of possible (callIndex, deliverynode) from a origin node
        """
        liste = []
        for (index, callOrigin, dest, _, _, _, _, _, _) in self.getCalls():
            if callOrigin == origin:
                liste.append((index, dest))
        return liste

    def getNumCalls(self):
        """
        num calls
        """
        return self.num_calls

    def getCompatibleCalls(self):
        """
        map from vehicle num to list of compatible calls
        """
        return self.compatibleCalls

    def getVehicles(self):
        """
        vehicle num, home node, start time, capacity
        """
        return self.vehicles

    def getVehiclesDict(self):
        """
        vehicle num => home node, start time, capacity
        :rtype: dict
        """
        return self.vehiclesDict

    def getCalls(self):
        """
        index, origin, destination, size, fail cost, lowerbound time pickup , upperbound time pickup, lowerbound time delivery, upperbuond time delivery
        """
        return self.calls

    def getCallsDict(self):
        """
        map form callNumber => origin, destination, size, fail cost, lowerbound time pickup , upperbound time pickup, lowerbound time delivery, upperbuond time delivery
        :return: dict
        """
        return self.callsDict

    def getVertexDict(self):
        """
        map from (vehicle, oridin, destination) => (travel time, travel cost)
        """
        return self.vertex

    def travelTime(self, vehicleNum, origin, dest):
        time, cost = self.vertex[vehicleNum, origin, dest]
        return time

    def travelCost(self, vehicleNum, origin, dest):
        _, cost = self.vertex[vehicleNum, origin, dest]
        return cost

    def getNodes(self):
        """
        map from (car num, call num) to:
        origin node time (in hours), origin node costs (in �), destination node time (in hours), destination node costs (in �)
        time is minus 1 if not compatible
        """
        return self.nodecost

    def isCompatible(self, car, call):
        compatible = self.getCompatibleCalls()
        return call in compatible[car]

    def readfile(self, name):
        fil = open(name)
        fil.readline()
        self.num_nodes = int(fil.readline())
        fil.readline()
        self.num_vehicles = int(fil.readline())
        fil.readline()
        # vehicles
        while True:
            line = fil.readline()
            if line[0] == '%':
                break
            i, home, time, cap = tuple([int(x) for x in line.split(",")])
            self.vehicles.append((i, home, time, cap))
            self.vehiclesDict[i] = (home, time, cap)
        # num calls
        self.num_calls = int(fil.readline())
        fil.readline()
        # list of calls that can be transported using that vehicle
        while True:
            line = fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.compatibleCalls[vals[0]] = vals[1:]
        # calls
        while True:
            line = fil.readline()
            if line[0] == '%':
                break
            # i, origin, dest, size, cost penalty, lowerpickup, upperpickup, lowerdel, upperdel
            i, origin, dest, s, c, lp, up, ld, ud = tuple(
                [int(x) for x in line.split(",")])
            self.calls.append((i, origin, dest, s, c, lp, up, ld, ud))
            self.callsDict[i] = (origin, dest, s, c, lp, up, ld, ud)
        # travel time and cost
        while True:
            line = fil.readline()
            if line[0] == '%':
                break
            v, o, d, t, c = tuple([int(x) for x in line.split(",")])
            self.vertex[(v, o, d)] = (t, c)
        # nodes
        while True:
            line = fil.readline()
            if line[0] == '%':
                break
            vehicle, call, origintime, origincosts, destinationtime, destinationcosts = tuple(
                [int(x) for x in line.split(",")])
            self.nodecost[(vehicle, call)] = (
                origintime, origincosts, destinationtime, destinationcosts)
