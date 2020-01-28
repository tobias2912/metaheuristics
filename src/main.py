from reader import Reader
#solution
carRoutes = []
#not visited nodes
notVisited = []
reader = Reader()
freeCalls=[]
def main():
    print("starting")
    reader.readfile("Call_7_Vehicle_3.txt")
    generateSolution()
    print(carRoutes)


def generateSolution():
    freeCalls=list(range(1, reader.getNumCalls()+1))
    for carN, home, start, cap in reader.getVehicles():
        #car n does all possible calls
        route=[]
        for callN, origin, dest, size, cost, lowerPickup, upperPickup, lowerDel, upperDel  in reader.getCalls():
            if isCompatible(carN, callN) and callN in freeCalls:
                freeCalls.remove(callN)
                route.append(origin)
                route.append(dest)
        carRoutes.append(route)


def isCompatible(car, call):
    compatible = reader.getCompatibleCalls()
    return call in compatible[car]








if __name__=="__main__":
    main()

    



