# metaheuristics

## solution representation:
a list of calls for each car separated with a 0. 
first call is implicit pickup and second is delivery. 
Last car is dummy car representing calls not delivered
- fixed length of 2 x calls+number of vehicles
- number of 0's = number of cars
- 2 occurrences of each call

## feasibility
- vehicle capacity
- pickup delivery by same vehicle
- time window between pickup and delivery
- wait for pickup if arrive early
- vehicle compatibility