import random
import time

class Bee:
    def __init__(self, position):
        self.position = position
        self.value = 0

def fitness(position):
    total_value = 0
    total_weight = 0
    for i in range(len(position)):
        if position[i] == 1:
            total_value += values[i]
            total_weight += weights[i]
            if total_weight > max_weight:
                return 0
    return total_value

def generate_random_bee(num_items):
    return Bee([random.randint(0, 1) for _ in range(num_items)])

def generate_neighboring_bee(bee):
    neighbor = Bee(bee.position.copy())
    index = random.randint(0, len(neighbor.position) - 1)
    neighbor.position[index] = 1 - neighbor.position[index]
    neighbor.value = fitness(neighbor.position)
    return neighbor

def search(bee_count, num_items, max_iterations):
    global values, weights, max_weight
    bees = [generate_random_bee(num_items) for _ in range(bee_count)]
    best_solution = None
    best_fitness = 0

    for _ in range(max_iterations):
        for bee in bees:
            neighbor = generate_neighboring_bee(bee)
            if neighbor.value > bee.value:
                bee.position = neighbor.position
                bee.value = neighbor.value
            if bee.value > best_fitness:
                best_solution = bee.position.copy()
                best_fitness = bee.value

    return best_solution, best_fitness

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n, max_weight = map(int, lines[0].split())
        values = []
        weights = []
        for line in lines[1:]:
            value, weight = map(int, line.split())
            values.append(value)
            weights.append(weight)
    return n, max_weight, values, weights

def write_output(filename, solution, fitness,execution_time):
    with open(filename, 'a') as file:
        file.write(f"{fitness} {solution}\n")
        file.write("Time {}\n".format(execution_time))

start_time = time.time()

def main():
    global values, weights, max_weight
    input_file = "ks_19_0.txt"
    output_file = "knapsack_artificialbee.txt"
    n, max_weight, values, weights = read_input(input_file)
    bee_count = 50
    max_iterations = 1000

    random.seed(42)
    solution, fitness = search(bee_count, n, max_iterations)

    end_time= time.time()
    execution_time= end_time - start_time

    write_output(output_file, solution, fitness,execution_time)
    

if __name__ == "__main__":
    main()
