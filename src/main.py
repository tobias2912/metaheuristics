import math
import random
import numpy as np
import time
import operators as ops
from feasibility import Feasibility
from reader import Reader

data = Reader()
feasibel = Feasibility(data)

files = ["data/Call_7_Vehicle_3.txt", "data/Call_18_Vehicle_5.txt", "data/Call_035_Vehicle_07.txt",
         "data/Call_080_Vehicle_20.txt", "data/Call_130_Vehicle_40.txt"]

operators = {ops.greedy_two_exchange: 92, ops.one_reinsert: 1400, ops.two_exch: 98, ops.threeExch: 5,
             ops.assign_unused_call: 242, ops.reduce_wait_two_ex: 4, ops.greedy_one_reinsert: 400}


def main():
    # automate_weights()
    #test_annealing()
    benchmark()
    #test_all()
    # data.readfile("data/Call_7_Vehicle_3.txt")  # 2,5M er best
    # init = [3, 3, 0, 0, 1, 1, 6, 6, 0, 4, 2, 4, 2, 5, 5]
    # print("\n", ops.assign_unused_call(init, data, feasibel))


"""
def automate_weights():
    cur_ops = operators.copy()
    iterations = 100
    record_improvment = 62
    for tries in range(1, iterations):
        change = 2 + round((iterations - tries) / 20)
        print("start nr ", tries, "     change:", change)
        op_num = random.randint(0, len(cur_ops) - 1)
        o, w, = cur_ops[op_num]
        if random.random() < 0.5:
            new_weight = w + change
        else:
            new_weight = w - change
        test_ops = cur_ops.copy()
        test_ops[op_num] = o, max(0, new_weight)
        improvements = []
        for _ in range(1):
            for file in files[1:4]:
                data.readfile(file)
                init_solution = create_init_solution()
                init_total = feasibel.total_cost(init_solution)
                _, objective = annealing_setup(init_solution, op=test_ops)
                improvements.append((100 * (init_total - objective) / init_total))
        improvement = sum(improvements) / len(improvements)
        if improvement > record_improvment:
            f, fw = cur_ops[op_num]
            print(f.__name__, fw, "was set to weight", new_weight, "(", round(improvement - record_improvment, 2),
                  "better), record is ", round(improvement, 1))
            record_improvment = improvement
            cur_ops = test_ops

            __print_operators(cur_ops)
        else:
            continue
    print("\n finished \n", cur_ops)
"""


def benchmark():
    num_iterations = 2
    improvements = []
    for file in files[1:4]:
        print(file)
        data.readfile(file)
        init_solution = create_init_solution()
        init_total = feasibel.total_cost(init_solution)
        # annealing
        annealing_solutions, best_total, runtime, best_solution = run_heuristic(annealing_setup, num_iterations,
                                                                                init_solution)
        print("total: ", best_total, "runtime", runtime)
        print("#################")
        improvements.append(round(100 * (init_total - best_total) / init_total))
    print("----------------\navg improvement: ", sum(improvements)/3)


def test_annealing():
    iterations = 1
    # data.readfile("data/Call_7_Vehicle_3.txt")  # 14 er best
    #data.readfile("data/Call_18_Vehicle_5.txt")  # 2,5M er best
    data.readfile("data/Call_035_Vehicle_07.txt")  # 5M er best
    #data.readfile("data/Call_080_Vehicle_20.txt")  # 13M er best
    # data.readfile("data/Call_130_Vehicle_40.txt")  # 13M er best
    sol, best, runtime, best_solution = run_heuristic(annealing_setup, iterations, create_init_solution())
    init_cost = feasibel.total_cost(create_init_solution())
    print("\n\n annealing test result")
    print("avg {} best {} time {:.3}, improvement {}".format(round(sum(sol) / iterations), best, runtime, round(100 * (init_cost - best) / init_cost)))
    #print(best_solution)


def run_heuristic(func, num_iterations, init_solution):
    """
    time is per iteration
    :rtype: solution, best objective, time
    """
    solution_objectives = []
    best_sol = []
    bestTotal = feasibel.total_cost(init_solution)
    start = time.time()
    for _ in range(num_iterations):
        sol, total = func(init_solution)
        if total < bestTotal:
            bestTotal = total
            best_sol = sol
        solution_objectives.append(total)
    end = time.time()
    return solution_objectives, bestTotal, (end - start) / num_iterations, best_sol


def annealing_setup(init_solution):
    iterations = 10000
    pMax = 0.9
    pMin = 0.1
    a = 0.9984
    op = operators.copy()
    minDelta, maxDelta = get_delta_e()
    t1 = -minDelta / np.log(pMax)
    t2 = -maxDelta / np.log(pMax)
    t3 = -minDelta / np.log(pMin)
    t4 = -maxDelta / np.log(pMin)
    start_temp = max(t1, t2, t3, t4)
    # endTemp = min(t1, t2, t3, t4)
    # print("starttemp", round(start_temp), "endtemp", round(endTemp), "a", a)
    solution, objective = simulated_annealing(init_solution, start_temp, a, op, iterations)
    return solution, objective


def escape_condition():
    """
    number of iterations without improvement to escape
    """
    return 20


def update_operators(weighted_ops, selected_operator, score):
    """
    increase/decrease weight of current operator
    """
    for operator, w, in weighted_ops.items():
        if operator == selected_operator:
            weighted_ops[operator] = w + max(score, 5)
            continue


def escape(incumbent):
    """
    do reinserts and move calls to dummy to diversify
    """
    call_percentage = 5
    iterations = math.floor(data.num_calls/100*call_percentage)
    for _ in range(iterations):
        incumbent = ops.move_to_dummy(incumbent, data, feasibel)
    incumbent = ops.n_exchange(incumbent, data, feasibel, n=iterations*5)
    return incumbent


def simulated_annealing(init_solution, temp_start, a, weighted_ops: dict, iterations=10000):
    """
    :param init_solution: random solution
    :param temp_start: start temperature
    :param a: cooling
    :param iterations: default 10k
    :param weighted_ops: list of (operator, weight)
    """
    incumbent = init_solution.copy()
    best_solution = init_solution.copy()
    temp = temp_start
    counter = Counter(weighted_ops)
    worse_iterations = 0
    prev_record = None
    all_records = []
    for i in range(iterations):
        if i % 2000 == 0:
            counter.update()
            #__print_operators(weighted_ops)
            print(len(all_records))
        if worse_iterations > escape_condition():
            counter.inc_escape()
            incumbent = escape(incumbent)
            worse_iterations = 0
            continue
        # try to generate feasible solution
        current_operator = select_operator(weighted_ops)
        for _ in range(10):
            new_solution = current_operator(incumbent, data, feasibel)
            if feasibel.is_feasible(new_solution):
                break
        if not feasibel.is_feasible(new_solution):
            counter.update_infeasible_operator(current_operator)
            update_operators(weighted_ops, current_operator, -1)
            continue
        else:
            counter.inc_feasible()
        if new_solution == incumbent:
            counter.inc_no_changes()
            update_operators(weighted_ops, current_operator, -1)
            continue
        if new_solution in all_records:
            incumbent = ops.n_exchange(incumbent, data, feasibel)
            worse_iterations = 0
            continue
        delta_e = feasibel.total_cost(new_solution) - feasibel.total_cost(incumbent)
        if delta_e < 0:
            # accept better
            if prev_record is not None:
                all_records.remove(prev_record)
            all_records.append(new_solution)
            prev_record = new_solution

            update_operators(weighted_ops, current_operator, 1)
            worse_iterations = 0
            incumbent = new_solution.copy()
            counter.inc_better()
            if feasibel.total_cost(incumbent) < feasibel.total_cost(best_solution):
                update_operators(weighted_ops, current_operator, 10)
                counter.inc_record()
                best_solution = incumbent.copy()
        elif random.random() < math.e ** (-delta_e / temp):
            prev_record = None
            # randomly accept worse
            worse_iterations += 1
            if delta_e != 0:
                counter.inc_random_accepts()
            incumbent = new_solution.copy()
        else:
            update_operators(weighted_ops, current_operator, -1)
            worse_iterations += 1
        temp = temp * a
    counter.append_all()

    # print("\nannealing search results:")
    # print("temperature ended at ",temp)
    # print("best objective is ", feasibel.total_cost(best_solution))
    # print("no changes by operator:", no_changes1, no_changes2, no_changes3
    print(counter)
    # counter.print_not_feasible_operators()
    return best_solution, feasibel.total_cost(best_solution)


def __print_operators(op_list, percent=True):
    out = ""
    total_weight = sum([w for _, w in op_list.items()])
    for op, we in op_list.items():
        out += "{:25}: ".format(op.__name__)
        if percent:
            out += "{:5}%".format(round((we / total_weight*100), 1))
        else:
            out += str(we)
        out+="\n"
    print(out)


def select_operator(weighted_ops):
    """
    choose heuristic based on performance
    """
    # (operator, weight)
    total_weight = sum([w for k, w in weighted_ops.items()])
    r = math.ceil(random.randint(0, total_weight))
    counter = 0
    for op, w in weighted_ops.items():
        counter += w
        if r <= counter:
            return op
    raise Exception(counter, r)


def test_all():
    num_iterations = 10
    for file in files:
        print("\n\nopening file", file, "\n\n")
        data.readfile(file)
        init_solution = create_init_solution()
        init_total = feasibel.total_cost(init_solution)
        # random
        # random_solutions, best_total, runtime, best_solution = run_heuristic(random_search, num_iterations,
        #                                                                     init_solution)
        # print("random search avg: ", sum(random_solutions) / num_iterations, "best", best_total)
        # print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        # local search
        # local_solutions, best_total, runtime, best_solution = run_heuristic(local_search, num_iterations, init_solution)
        # print("local search avg: ", sum(local_solutions) / num_iterations, "best", best_total)
        # print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        # annealing
        annealing_solutions, best_total, runtime, best_solution = run_heuristic(annealing_setup, num_iterations,
                                                                                init_solution)
        print("annealing search avg: ", sum(annealing_solutions) / num_iterations, "best", best_total)
        print("improvement:", round(100 * (init_total - best_total) / init_total), " time: ", round(runtime))
        print(best_solution)


def get_delta_e():
    """
    do some reinserts to guess deltaE
    """
    diff = []
    sol = generateSolution()
    for _ in range(10):
        newsol = ops.one_reinsert(sol, data, feasibel)
        t1 = feasibel.total_cost(newsol)
        t2 = feasibel.total_cost(sol)
        d = abs(t2 - t1)
        if d != 0:
            diff.append(abs(t2 - t1))
        sol = newsol
    assert len(diff) > 1, len(diff)
    return np.percentile(diff, 10), np.percentile(diff, 90)


class Counter:
    better_count, random_accepts_count, no_changes, no_changes2, no_changes3, feasible_count, record_count = 0, 0, 0, 0, 0, 0, 0
    feasible_list = []
    random_accepts_list = []
    better_count_list = []
    record_list = []

    def __init__(self, weighted_ops: dict):
        self.escape_count = 0
        self.better_count, self.random_accepts_count, self.no_changes, self.no_changes2 = 0, 0, 0, 0
        self.no_changes3, self.feasible_count, self.record_count = 0, 0, 0
        self.feasible_list, self.random_accepts_list, self.better_count_list = [], [], []
        self.escape_count_list, self.record_list = [], []
        self.not_feasible_operators = {}
        for op, w in weighted_ops.items():
            self.not_feasible_operators[op.__name__] = 0

    def update_infeasible_operator(self, operator):
        self.not_feasible_operators[operator.__name__] = self.not_feasible_operators[operator.__name__] + 1

    def update(self):
        self.random_accepts_list.append(self.random_accepts_count)
        self.better_count_list.append(self.better_count)
        self.feasible_list.append(self.feasible_count)
        self.record_list.append(self.record_count)
        self.escape_count_list.append(self.escape_count)
        self.better_count, self.random_accepts_count, self.feasible_count, self.record_count, self.escape_count = 0, 0, 0, 0, 0

    def inc_feasible(self):
        self.feasible_count += 1

    def append_all(self):
        self.random_accepts_list.append(self.random_accepts_count)
        self.better_count_list.append(self.better_count)
        self.feasible_list.append(self.feasible_count)
        self.record_list.append(self.record_count)
        self.escape_count_list.append(self.escape_count)
        self.record_list.pop(0)
        self.random_accepts_list.pop(0)
        self.better_count_list.pop(0)
        self.feasible_list.pop(0)
        self.escape_count_list.pop(0)

    def inc_no_changes(self):
        self.no_changes += 1

    def inc_better(self):
        self.better_count += 1

    def inc_record(self):
        self.record_count += 1

    def inc_random_accepts(self):
        self.random_accepts_count += 1

    def inc_escape(self):
        self.escape_count += 1

    def __repr__(self):
        out = "no changes: " + str(self.no_changes)
        out += ("\nfeasible, better, random, record, escapes\n")
        for i in range(len(self.feasible_list)):
            out += ('   {:7}{:7}{:7}{:7}{:7}\n'.format(self.feasible_list[i], self.better_count_list[i],
                                                       self.random_accepts_list[i], self.record_list[i],
                                                       self.escape_count_list[i]))
        return out

    def print_not_feasible_operators(self):
        print("operators amount not feasible")
        print(self.not_feasible_operators)


def create_init_solution():
    solution = [0 for _ in range(data.num_cars)]
    solution += list(range(1, data.num_calls + 1))
    solution += list(range(1, data.num_calls + 1))
    return solution


def local_search(init_solution, p1=0.3, p2=0.3, iterations=10000):
    best_solution = init_solution.copy()
    for _ in range(iterations):
        rand = ops.random.random()
        if rand < p1:
            current = ops.two_exch(best_solution, data.num_cars)
        elif rand < p1 + p2:
            current = ops.threeExch(best_solution, data.num_cars)
        else:
            current = ops.one_reinsert(best_solution, data.num_cars, data.num_calls)
        if feasibel.is_feasible(current) and feasibel.total_cost(current) < feasibel.total_cost(best_solution):
            best_solution = current
    # print("localsearch best is ", totalCost(best_solution), " - ", best_solution)
    return best_solution, feasibel.total_cost(best_solution)


def random_search(initSolution, iterations=10000):
    bestSolution = initSolution.copy()
    for _ in range(iterations):
        currentSolution = generateRandom()
        if feasibel.is_feasible(currentSolution) and feasibel.total_cost(currentSolution) < feasibel.total_cost(
                bestSolution):
            bestSolution = currentSolution
    # print("randomsearch best is", totalCost(bestSolution), " - ", bestSolution)
    # assert len(initSolution) == data.numCalls * 2 + data.num_vehicles
    return bestSolution, feasibel.total_cost(bestSolution)


def generateSolution():
    """
    generate empty start solution
    """
    car_calls = []
    free_calls = list(range(1, data.getNumCalls() + 1))
    for carN, home, start, cap in data.getVehicles():
        # car n does all possible calls
        current_time = start
        current_node = home
        current_capacity = 0
        for callN, origin, dest, size, _, lowerPickup, upperPickup, lowerDel, upperDel in data.getCalls():
            if data.isCompatible(carN, callN) and callN in free_calls and current_capacity + size <= cap:
                # time constraint
                pickuptime = current_time + \
                             data.travelTime(carN, current_node, origin)
                deliverytime = pickuptime + \
                               data.travelTime(carN, origin, dest)
                if lowerPickup <= pickuptime <= upperPickup and lowerDel <= deliverytime <= upperDel:
                    free_calls.remove(callN)
                    car_calls.append(callN)
                    car_calls.append(callN)
                    current_node = dest
                    current_time = deliverytime

        car_calls.append(0)
    # dummy car
    car_calls.extend(free_calls)
    car_calls.extend(free_calls)
    return car_calls


def generateRandom():
    car = {}
    num_vehicles = data.num_cars + 1
    for carN in range(1, num_vehicles + 1):
        car[carN] = []
    calls = range(1, data.getNumCalls() + 1)
    # map random car to all call pairs
    for call in calls:
        car_calls = car[math.ceil(random.random() * num_vehicles)]
        car_calls.append(call)
        car_calls.append(call)
    # shuffle order of delivery
    solution = []
    for carN in range(1, num_vehicles + 1):
        car_calls = car[carN]
        random.shuffle(car_calls)
        solution += car_calls
        solution += [0]
    solution.pop()
    return solution


if __name__ == "__main__":
    main()
