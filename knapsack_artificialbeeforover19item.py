import random
import time

class Bee:
    def __init__(self, items, max_weight):
        self.items = items
        self.max_weight = max_weight
        self.value = 0
        self.weight = 0
        self.selected_items = []
        self.generate_solution()

    def generate_solution(self):
        self.selected_items = [random.choice([0, 1]) for _ in range(len(self.items))]
        self.calculate_fitness()

    def calculate_fitness(self):
        self.value = sum(self.items[i][0] for i in range(len(self.items)) if self.selected_items[i] == 1)
        self.weight = sum(self.items[i][1] for i in range(len(self.items)) if self.selected_items[i] == 1)

class ABC:
    def __init__(self, items, max_weight, colony_size=50, max_iterations=100):
        self.items = items
        self.max_weight = max_weight
        self.colony_size = colony_size
        self.max_iterations = max_iterations
        self.optimal_solution = None
        self.initialize_colony()

    def initialize_colony(self):
        self.colony = [Bee(self.items, self.max_weight) for _ in range(self.colony_size)]
        self.optimal_solution = max(self.colony, key=lambda bee: bee.value)

    def employeed_bees_phase(self):
        for bee in self.colony:
            neighbor_bee = self.get_random_neighbor_bee(bee)
            self.explore_neighbor(bee, neighbor_bee)

    def get_random_neighbor_bee(self, current_bee):
        neighbor_bee = current_bee
        while neighbor_bee == current_bee:
            neighbor_bee = random.choice(self.colony)
        return neighbor_bee

    def explore_neighbor(self, current_bee, neighbor_bee):
        new_solution = self.local_search(current_bee, neighbor_bee)
        if new_solution.value > current_bee.value and new_solution.weight <= self.max_weight:
            current_bee.selected_items = new_solution.selected_items
            current_bee.value = new_solution.value
            current_bee.weight = new_solution.weight

    def local_search(self, bee1, bee2):
        selected_items = []
        for i in range(len(bee1.selected_items)):
            selected_items.append(bee1.selected_items[i] if random.random() < 0.5 else bee2.selected_items[i])
        return self.create_bee(selected_items)

    def create_bee(self, selected_items):
        bee = Bee(self.items, self.max_weight)
        bee.selected_items = selected_items
        bee.calculate_fitness()
        return bee

    def onlooker_bees_phase(self):
        probabilities = [bee.value / self.optimal_solution.value if bee.weight <= self.max_weight else 0 for bee in self.colony]
        probabilities_sum = sum(probabilities)
        if probabilities_sum == 0:
            probabilities = [1 / self.colony_size for _ in range(self.colony_size)]
        else:
            probabilities = [prob / probabilities_sum for prob in probabilities]
        for _ in range(self.colony_size):
            bee = self.select_bee(probabilities)
            neighbor_bee = self.get_random_neighbor_bee(bee)
            self.explore_neighbor(bee, neighbor_bee)

    def select_bee(self, probabilities):
        r = random.uniform(0, 1)
        partial_sum = 0
        for i in range(len(probabilities)):
            partial_sum += probabilities[i]
            if partial_sum >= r:
                return self.colony[i]

    def scout_bees_phase(self):
        for bee in self.colony:
            if bee.weight > self.max_weight:
                bee.generate_solution()

    def optimize(self):
        for _ in range(self.max_iterations):
            self.employeed_bees_phase()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            self.update_optimal_solution()

    def update_optimal_solution(self):
        best_bee = max(self.colony, key=lambda bee: bee.value)
        if best_bee.value > self.optimal_solution.value and best_bee.weight <= self.max_weight:
            self.optimal_solution = best_bee

    def solve_knapsack_problem(self):
        self.optimize()
        optimal_value = self.optimal_solution.value
        selected_items = [1 if i in self.optimal_solution.selected_items else 0 for i in range(len(self.items))]
        return optimal_value, selected_items


def read_knapsack_file(filename):
    with open(filename, "r") as f:
        max_items, max_weight = map(int, f.readline().split())
        items = []
        for line in f:
            value, weight = map(int, line.split())
            items.append((value, weight))
    return items, max_weight

def write_output(filename, solution, fitness,selected_indices,execution_time):
    with open(filename, 'a') as file:
        file.write(f"{fitness} {solution}\n")
        file.write("Selected Indices: {}\n".format(selected_indices))
        file.write("Time: {}\n".format(execution_time))

start_time = time.time()

def main():

    items, max_weight = read_knapsack_file("ks_10000_0.txt")
    output_file = "knapsack_artificialbee.txt"
    abc = ABC(items, max_weight)
    optimal_value, selected_items = abc.solve_knapsack_problem()
    print("Optimal value:", optimal_value)
    print("Selected items:", selected_items)
    selected_indices = [i for i in selected_items]
    print("Selected item indices:", selected_indices)

    end_time=time.time()
    execution_time= end_time - start_time

    write_output(output_file,selected_items,optimal_value,selected_indices, execution_time)

    

if __name__ == "__main__":
    main()

       
