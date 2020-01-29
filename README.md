## metaheuristics

# løsningsrepresentasjon:
en liste med calls for hver bil, separert med 0 mellom bilene. implisitt første call er pickup, andre like call er delivery. implisitt start og retur fra home node. [4, 4, 3, 3]
siste "bilen" er en liste med calls som ikke er besøkt.
må være par av calls og ingen repeterende

- fixed lengde 
- antall 0 = antall biler
- nøyaktig 2 av hver call

# feasibility
- vehicle capacity
- pickup delivery by same vehicle
- time window between pickup and delivery
- wait for pickup if arrive early
- vehicle compatibility