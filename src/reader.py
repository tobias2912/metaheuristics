class Reader:
    
    def __init__(self):
        self.num_nodes=0
        self.num_vehicles=0
        self.vehicles = []
        self.calls=[]
        self.travel=[]
        self.nodecost=[]

    def getVehicles(self):
        return self.vehicles

    def readfile(self, name):
        fil = open(name)
        fil.readline()
        num_nodes=int(fil.readline())
        fil.readline()
        num_vehicles=int(fil.readline())
        fil.readline()
        #vehicle index, home node, starting time, capacity
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.vehicles.append(vals)
        #call index, origin node, destination node, size, cost of not transporting, lowerbound timewindow for pickup, upper_timewindow for pickup, lowerbound timewindow for delivery, upper_timewindow for delivery
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.calls.append(vals)
        #travel times and costs: vehicle, origin node, destination node, travel time (in hours), travel cost (in �)
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.travel.append(vals)
        #node times and costs: vehicle, call, origin node time (in hours), origin node costs (in �), destination node time (in hours), destination node costs (in �)
        while(True):
            line=fil.readline()
            if line[0] == '%':
                break
            vals = [int(x) for x in line.split(",")]
            self.nodecost.append(vals)
