class Reader:
    
    def __init__(self):
        self.cars = []

    def readfile(self, name):
        fil = open(name)
        while True:
            #read first
            line = fil.readline()
            if line[0] == '%':
                break
            values = line.split(",")
            self.cars.append(values)
        return self.cars


