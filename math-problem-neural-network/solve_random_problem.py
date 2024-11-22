import random
import time

from pprint import pprint

# pick random constants for math problem
# for more consistent results, change the range to (1, 15)
A = random.uniform(-15, 15)
B = random.uniform(-15, 15)
C = random.uniform(-15, 15)

EXP_X = random.uniform(-15, 15)
EXP_Y = random.uniform(-15, 15)
EXP_Z = random.uniform(-15, 15)


def get_solution_string(x, y, z, equals_to = 0):
    return f"{A} * {x} ** {EXP_X} + {B} * {y} ** {EXP_Y} + {C} * {z} ** {EXP_Z} = {equals_to}"


def print_f(equals_to = 0):
    print(f"{A} * x ** {EXP_X} + {B} * y ** {EXP_Y} + {C} * z ** {EXP_Z} = {equals_to}")


def f(x, y, z, equals_to = 0):
    return A * x ** EXP_X + B * y ** EXP_Y + C * z ** EXP_Z + equals_to


def calculate_fitness(x, y, z, equals_to = 0):
    answer = f(x, y, z, equals_to)

    if answer == 0:
        return float('inf')
    return abs(1 / answer)
    
    # return abs(1 / answer) if answer else 999999  # higher if it's closer to 0


def get_initial_solutions(n = 1000):
    solutions = []
    
    for _ in range(n):
        # random values for x, y, z 
        solutions.append(
            (random.uniform(1, 1000), random.uniform(1, 1000), random.uniform(1, 1000))
        )

    return solutions


def run_genetic_algorithm(population_size = 1000, how_many_generations = 10000):
    pass


def print_best_solution_of_the_generation(generation_n, best_solution):
    print(f"\n\n  ===  Best Fitness of Generation {generation_n}  ===  ")
    print(f"x = {best_solution[1][0]}")
    print(f"y = {best_solution[1][1]}")
    print(f"z = {best_solution[1][2]}")
    answer = f(*best_solution[1])
    print(f"f(x, y, z) = {answer}")
    # best_solution_string = get_solution_string(*best_solution[1])
    # print(f"Wanted solution : {best_solution_string}")
    best_solution_string_with_actual_solution = get_solution_string(*best_solution[1], answer)
    print(f"{best_solution_string_with_actual_solution}")
    print(f"Fitness : {best_solution[0]}")


def main(population_size = 1000, max_generations = 50000, mutation_chance = 0.01): 
    """
    Main function to run a genetic algorithm.

    Parameters:
        population_size (int): The number of individuals in the population. Default is 1000.
        max_generations (int): The maximum number of generations to evolve. Default is 10000.
        mutation_chance (float): The probability of mutation for each individual. 
                                 It's recommended to keep this value low to avoid excessive random changes.
                                 Default is 0.01.
    
    Returns:
        best_solution (tuple): Best solution with fitness and x, y, z values.
        generation_n (int): Number of generations passed to find the best_solution.
    """
    initial_solutions = get_initial_solutions()

    solutions = []
    for solution in initial_solutions:
        fitness = calculate_fitness(*solution)
        solutions.append((fitness, solution))
        # print(f"Fitness: {fitness}")

    # sort by the fitness
    solutions.sort(reverse=True)

    best_solutions = solutions[:100]  # top 100 of the last generation
    for generation_n in range(max_generations):

        print_best_solution_of_the_generation(generation_n, best_solutions[0])

        new_solutions = []

        for n in range(population_size):

            new_solutions.append(
                (
                    random.choice(best_solutions)[1][0] * random.uniform(1 - mutation_chance, 1 + mutation_chance),
                    random.choice(best_solutions)[1][1] * random.uniform(1 - mutation_chance, 1 + mutation_chance),
                    random.choice(best_solutions)[1][2] * random.uniform(1 - mutation_chance, 1 + mutation_chance),
                )
            )

        ranked_solutions = []
        for solution in new_solutions:
            fitness = calculate_fitness(*solution)
            ranked_solutions.append((fitness, solution))

        # sort by the fitness
        ranked_solutions.sort(reverse=True)
        best_solutions = ranked_solutions[:100]


        if best_solutions[0][0] > 1000:
            return best_solutions[0], generation_n
    
    print(f"{max_generations} generations exceeded!")
    return best_solution[0], max_generations



if __name__ == "__main__":
    try:
        print_f()
        # time.sleep(2)
        input("Press any key to start...")
        best_solution, generation_n = main()
        print_best_solution_of_the_generation("Final", best_solution)
        print(f"Found in {generation_n} generations.")
        # print(best_solution)
    except KeyboardInterrupt:
        exit()

"""  luckiest mutation ever
  ===  Best Fitness of Generation 2116  ===
x = 401.70050918397015
y = 3.573810708470632
z = 3.0224601940790823
f(x, y, z) = 94.0637759328747
-1.7770621650373517 * 401.70050918397015 ** 2.0459487079764616 + 2.2390506776246255 * 3.573810708470632 ** 9.468476392936545 + -7.9161170582592435 * 3.0224601940790823 ** 6.351513516575976 = 94.0637759328747
Fitness : 0.0106310850280305


  ===  Best Fitness of Generation 2117  ===
x = 396.5087733328378
y = 3.5706678241032113
z = 3.3052362777115207
f(x, y, z) = -3.158660460883766
-1.7770621650373517 * 396.5087733328378 ** 2.0459487079764616 + 2.2390506776246255 * 3.5706678241032113 ** 9.468476392936545 + -7.9161170582592435 * 3.3052362777115207 ** 6.351513516575976 = -3.158660460883766
Fitness : 0.31658990017566135


  ===  Best Fitness of Generation Final  ===
x = 406.28613154285347
y = 3.5831501657353715
z = 3.068389520134863
f(x, y, z) = 0.00018862310389522463
-1.7770621650373517 * 406.28613154285347 ** 2.0459487079764616 + 2.2390506776246255 * 3.5831501657353715 ** 9.468476392936545 + -7.9161170582592435 * 3.068389520134863 ** 6.351513516575976 = 0.00018862310389522463
Fitness : 5301.577480961583
Found in 2117 generations.
"""