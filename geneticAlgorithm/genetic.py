import numpy
import csv
import os

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
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
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

sol_per_pop = 15
num_parents_mating = 5
num_weights = 3

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
#Creating the initial population.
new_population = numpy.random.uniform(low=-20.0, high=20.0, size=pop_size)
print(new_population)

num_generations = 10
for generation in range(num_generations):
    print("Generation : ", generation)
    # Measing the fitness of each chromosome in the population.
    fit = []
    maxScore = -99999999999999
    idMax = ''
    winMax = -9999999999999
    scoreMax = -99999999999
    for ind in range(len(new_population)):
        print "_______________________________" 
        print ("G: ",generation, "Ind:", ind)
        print "_______________________________"
        with open('weights.txt', 'a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            employee_writer.writerow([generation,ind,new_population[ind][0],new_population[ind][1], new_population[ind][2]])
        
        os.system('python pacman.py -p ReflexAgent -l originalClassic -q -n 5')

        with open('scores.txt', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                g = int(row['geration'])
                id = int(row['id'])
                averageScore = float(row['averageScore'])
                winRate = row['winRate']
        winRate = float(winRate)
        score = averageScore + (averageScore * winRate)
        if(score > maxScore):
            maxScore = score
            idMax = "Gen: " + str(g) + " id: " + str(id)
            scoreMax = averageScore,
            winMax = winRate
        fit.append(averageScore)
    fitness = numpy.array(fit)
    parents = select_mating_pool(new_population, fitness, 
                                      num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents,
                                       offspring_size=(pop_size[0]-parents.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    # The best result in the current iteration.
    best = "Best result : " + str(maxScore) + " " + idMax
    print best
    with open('results.txt', 'a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            employee_writer.writerow([best,winMax,scoreMax])

