class Reader:
    
    def __init__(self):
        self.num_nodes=0
        self.num_vehicles=0
        self.vehicles = []
        self.calls=[]
        self.compatibleCalls={}
        self.travel=[]
        self.nodecost={}

    def getNumCalls(self):
        """
        num calls
        """
        return self.numCalls
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

    def getCalls(self):
        """
        index, origin, destination, size, fail cost, lowerbound time pickup , upperbound time pickup, lowerbound time delivery, upperbuond time delivery
        """
        return self.calls

    def getVertex(self):
        """
        vehicle, origin , destination , travel time, travel cost
        """
        return self.travel

    def getNodes(self):
        """
        map from (car num, call num) to:
        origin node time (in hours), origin node costs (in �), destination node time (in hours), destination node costs (in �)
        time is -1 if not compatible
        """
        return self.nodecost

    def readfile(self, name):
        fil = open(name)
        fil.readline()
        num_nodes=int(fil.readline())
        fil.readline()
        num_vehicles=int(fil.readline())
        fil.readline()
        #vehicles
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.vehicles.append(tuple(vals))
        #num calls
        self.numCalls = int(fil.readline())
        fil.readline()
        #list of calls that can be transported using that vehicle
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.compatibleCalls[vals[0]]=vals[1:]
        #calls
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.calls.append(tuple(vals))
        #travel time and cost
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.travel.append(tuple(vals))
        #nodes
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vehicle, call, origintime, origincosts, destinationtime, destinationcosts = tuple([int(x) for x in line.split(",")])
            #self.nodecost.append(tuple(vals))
            self.nodecost[(vehicle, call)]= (origintime, origincosts, destinationtime, destinationcosts)
