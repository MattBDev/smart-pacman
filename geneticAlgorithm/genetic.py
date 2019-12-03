import numpy
import csv
import os
import pandas as pd
from statistics import mean, median


def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k % parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k + 1) % parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        gene = numpy.random.randint(3)
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, gene] = offspring_crossover[idx, gene] + random_value
    return offspring_crossover


def population_size(sol_per_pop, num_weights):
    # Defining the population size.
    pop_size = (sol_per_pop,
                num_weights)  # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    return pop_size


def initial_population(pop_size):
    # Creating the initial population.
    new_population = numpy.random.uniform(low=-20.0, high=20.0, size=pop_size)
    print(new_population)
    return new_population


def populational_test(generation, population):
    fit = []
    winRate = 0
    (maxScore, idMax, winMax, scoreMax) = (-99999999999999, '', -9999999999999, -99999999999)
    for ind in range(len(population)):
        print
        "_______________________________"
        print("G: ", generation, "Ind:", ind)
        print
        "_______________________________"
        with open('weights.txt', 'a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([generation, ind, population[ind][0], population[ind][1], population[ind][2]])
        os.system('python pacman.py -p ReflexAgent -l originalClassic -q -n 10')

    return populational_indicators(generation)


def populational_indicators(generation):
    individual_scores = pd.read_csv("scores.txt", delimiter=",")
    current_population = individual_scores[individual_scores["generation"] == generation]
    aux = [int(i) for i in current_population["averageScore"].tolist()]
    average_score = mean(aux)
    max_score = max(aux)
    min_score = min(aux)
    aux = [float(i) for i in current_population["winRate"].tolist()]
    population_winning_rate = median(aux)
    fit = numpy.array(aux)

    indicators = [fit, average_score, max_score, min_score, population_winning_rate]
    return indicators


def mutate_population(fitness, num_parents_mating, pop_size, population):
    parents = select_mating_pool(population, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], pop_size[1]))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    population[0:parents.shape[0], :] = parents
    population[parents.shape[0]:, :] = offspring_mutation
    return population


def set_files():
    with open('results.txt', 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['generation', 'average_score', 'best_score', 'worst_score', 'mean_winning_rate'])

    with open('scores.txt', 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['generation', 'id', 'w1', 'w2', 'w3', 'averageScore', 'winRate', 'scores'])

    with open('weights.txt', 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['geration', 'id', 'w1', 'w2', 'w3'])


def evolution_by_winning_rate_limit(winning_rate_limit, population, pop_size):
    generation = 0
    winning_rate = -9999

    set_files()

    while winning_rate < winning_rate_limit:
        print("Generation : ", generation)

        # Measing the fitness of each chromosome in the population.
        results = populational_test(generation, population)
        population = mutate_population(fitness=results[0], num_parents_mating=5, pop_size=pop_size,
                                       population=population)

        with open('results.txt', 'a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([generation, results[1], results[2], results[3], results[4]])

        generation += 1
        winning_rate = results[4]


def evolution_by_generation_limit(num_generations, population, pop_size):
    set_files()

    for generation in range(num_generations):
        print("Generation : ", generation)

        # Measing the fitness of each chromosome in the population.
        results = populational_test(generation, population)
        population = mutate_population(fitness=results[0], num_parents_mating=5, pop_size=pop_size,
                                       population=population)

        with open('results.txt', 'a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([generation, results[1], results[2], results[3], results[4]])


pop_size = population_size(15, 3)  # pop_size = (sol_per_pop,num_weights)
initial_pop = initial_population(pop_size)
evolution_by_generation_limit(64, initial_pop, pop_size)
#evolution_by_winning_rate_limit(0.3, initial_pop, pop_size)
