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
