from map_generator import *
import csv

iterations = [10, 100, 1000]
populations = [10, 100, 100]
mutations = [0.01, 0.05, 0.1]
map_sizes = [10, 11, 15, 20]

fname = "ga_experiment_at_" + str(int(time.time()))
log_file = open(fname + ".log", "w")

headers = [
    "test_id",
    "iterations",
    "population_size",
    "map_size",
    "mutation_rate",
    "experiment_duration",
    "best_fitness",
]

with open(fname + ".csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)

test = 1
for iteration in iterations:
    for population in populations:
        for mutation in mutations:
            for map_size in map_sizes:
                st = time.time()
                ga = GeneticAlgorithm(
                        population_size=population,
                        mutation_rate=mutation,
                        iterations=iteration,
                        map_size=map_size
                    )
                ga.evolve()
                filename = "iteration_" + str(iteration)
                filename += "_population_" + str(population)
                filename += "_mutation_" + str(mutation)
                filename += "_mapsize_" + str(map_size) + "_"
                et = time.time()
                ga.save_best_individuals(filename=filename)
                t = et - st
                
                test_log = {
                    "test_id": test,
                    "iterations": iteration,
                    "population_size": population,
                    "map_size": map_size,
                    "mutation_rate": mutation,
                    "experiment_duration": t,
                    "best_fitness": ga.population[0].get_fitness()
                }

                with open(fname + ".csv", "a") as csv_file:
                    wr = csv.writer(csv_file)
                    wr.writerow([test_log[col] for col in headers])

                log_file.write("# Test %d:\n %d iterations,\n %d population size,\n %d map side size,\n %f mutation rate\n %f seconds of experiment duration\n %f best fitness\n\n" % (test, iteration, population, map_size, mutation, t, ga.population[0].get_fitness()))
                test += 1

log_file.close()