# Program made by Rafael Pontes

from random import randint, random
import os, string

DEBUG = True
DEBUG_ITERATION = 2

tiles_dict = {
    "food": ".",
    "wall": "%",
    "pacman": "P",
    "specialfood": "o",
    "ghost": "G",
    "blank": " "
}
tiles = [".", "%"]
NUM_TILES = len(tiles)

class MapIndividual():

    available_id = 0

    def __init__(self, map_size = 10, mutation_rate = 0.05, matrix = None):
        self.id = MapIndividual.available_id
        MapIndividual.available_id += 1
        self.width = map_size
        self.height = map_size
        self.msize = map_size
        self.mutation_rate = mutation_rate
        if (matrix == None):
            self.generate_random_map()
        else:
            self.matrix = []
            for row in matrix:
                self.matrix.append([])
                for col in row:
                    self.matrix[-1].append(col)
            self.height = len(matrix)
            self.width = len(matrix[0])
            self.msize = map_size

    def __str__(self):
        s = " Individual id %d.\n" % (self.id)
        s += self.parse_map()
        s += " Fitness = %f\n" % (self.get_fitness())
        s += " Playble? %s\n" % (str(self.is_playable()))
        return s
        
    def generate_random_map(self):
        self.matrix = []
        for i in range(self.width):
            self.matrix.append(list())
            for j in range(self.height):
                border = [0, self.width - 1]
                if (i in border or j in border):
                    self.matrix[i].append(tiles_dict["wall"])
                else:
                    self.matrix[i].append(self.get_random_tile())

    def force_playable(self):
        while(not self.is_playable()):
            x = randint(1, self.msize - 2)
            y = randint(1, self.msize - 2)
            while (self.matrix[x][y] != tiles_dict["wall"]):
                x = randint(1, self.msize - 2)
                y = randint(1, self.msize - 2)
            self.matrix[x][y] = tiles_dict["food"]

    def get_fitness(self):
        score = 1000.0
        score += 1000.0 * int(self.is_playable())
        score -= 5.0 * self.tile_square_count(tiles_dict["wall"])
        score -= 5.0 * self.tile_square_count(tiles_dict["food"])
        score -= 5.0 * self.outer_wall_count()
        score -= 5.0 * self.diagonal_artifact_count()
        score = max(0.0, score)
        return score
    
    def diagonal_artifact_count(self):
        count = 0
        for i in range(1, self.msize - 2):
            for j in range(1, self.msize - 2):
                # main diagonal
                md = [self.matrix[i][j], self.matrix[i+1][j+1]]
                # secondary diagonal
                sd = [self.matrix[i+1][j], self.matrix[i][j+1]]
                if (md[0] == md[1] and sd[0] == sd[1] and md[0] != sd[0]):
                    count += 1
        return count


    def outer_wall_count(self):
        count = 0
        for i in range(1, self.width - 2):
            count += 0 if MazeCell(self.matrix[1][i]).is_walkable() else 1
            count += 0 if MazeCell(self.matrix[i][1]).is_walkable() else 1
            count += 0 if MazeCell(self.matrix[self.width-1][i]).is_walkable() else 1
            count += 0 if MazeCell(self.matrix[i][self.height-1]).is_walkable() else 1
        return count

    def get_neighbors(self, cell):
        x, y = cell.pos[0], cell.pos[1]
        if (x < 0) or (y < 0) or (x > self.width) or (y > self.height):
            # Ignore outer walls and invalid cells
            return []
        neigh = []
        points = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
        for point in points:
            cell = cell = self.get_cell((point[0], point[1]))
            if (cell != None):
                neigh.append(cell)
        return neigh

    def get_walkable_neighbors(self, cell):
        if (cell == None):
            return None
        return [ x for x in self.get_neighbors(cell) if x.is_walkable() ]

    def get_cell(self, pos):
        if pos == None:
            return None
        x, y = pos[0], pos[1]
        dims = self.get_dimensions()
        if (x < 0) or (y < 0) or (x > dims[0] - 1) or (y > dims[1] - 1):
            # Ignore invalid cells
            return None
        return MazeCell(self.matrix[x][y], (x, y))

    def get_dimensions(self):
        rows = len(self.matrix)
        if (rows > 0):
            cols = len(self.matrix[0])
        else:
            cols = 0
        return (rows, cols)

    def food_count(self):
        count = 0
        for row in self.matrix:
            for cell in row:
                if MazeCell(cell).is_food():
                    count += 1
        return count

    def get_next_cell(self, pos):
        if (pos == None):
            return None
        x, y = pos[0], pos[1]
        nx = (x + 1) % self.width
        ny = y if nx != 0 else y + 1
        return self.get_cell((nx, ny))

    def get_first_food(self):
        ccell = self.get_cell((0, 0))
        while (not ccell.is_food()):
            ccell = self.get_next_cell(ccell.pos)
        if (ccell.is_food()):
            return ccell
        return None

    def visit_all_neighbors(self, cell, visited):
        neighbors = self.get_walkable_neighbors(cell)
        if (neighbors == None):
            return
        for wn in neighbors:
            x, y = wn.pos[0], wn.pos[1]
            if (not visited[x][y]):
                # Recursively visit all reachable cells
                visited[x][y] = True
                self.visit_all_neighbors(MazeCell(self.matrix[x][y], (x, y)), visited)

    def is_playable(self):
        fcount = self.food_count()
        if fcount < (self.width * self.height / 3):
            return False

        visited = [ [False for i in range(self.width)] for j in range(self.height) ] # All with false
        for i in range(len(visited)):
            for j in range(len(visited[0])):
                # Mark all non-walkable cells as visited
                if not MazeCell(self.matrix[i][j]).is_walkable():
                    visited[i][j] = True
        # There is at least one food cell, no check required
        self.visit_all_neighbors(self.get_first_food(), visited)

        # Check if all are visited
        for i in range(len(visited)):
            for j in range(len(visited[0])):
                if (visited[i][j] == False):
                    # There's at least one unreachabled cell
                    return False
        return True
    
    def tile_square_count(self, tile):
        # Searches for square of same tile type
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.found_tile_square((i, j), tile):
                    count += 1
        return count
    
    def found_tile_square(self, pos, tile):
        x, y = pos[0], pos[1]
        points = [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]
        for point in points:
            cell = self.get_cell(point)
            if (cell == None or cell.tile == tile):
                return False
        return True

    def mutate(self):
        for i in range(1, self.width-1):
            for j in range(1, self.height-1):
                if (self.should_mutate()):
                    self.matrix[i][j] = self.get_random_tile()
    
    def get_random_tile(self):
        return tiles[randint(0, len(tiles)-1)]
    
    def get_random_cell(self):
        # Picks a random cell excluding outer walls
        rx = randint(1, self.width - 2)
        ry = randint(1, self.height - 2)
        return self.get_cell((rx, ry))

    def should_mutate(self):
        return (random() <= self.mutation_rate)
    
    def parse_map(self):
        s = ""
        for row in self.matrix:
            for col in row:
                s += col
            s += "\n"
        return s

class GeneticAlgorithm():
    def __init__(self, population_size = 100,
                        mutation_rate = 0.05,
                        iterations = 50,
                        elitism_factor = 0.5,
                        stop_criteria = "iterations",
                        playable_minimum = 1,
                        map_size = 10):
        self.elitism_factor = elitism_factor
        self.iterations = iterations
        self.psize = population_size
        self.mutation_rate = mutation_rate
        self.msize = map_size
        self.population = self.create_population(playable_minimum=playable_minimum, map_size=self.msize)

    def create_population(self, playable_minimum = 1, map_size = 10):
        population = []
        playable_count = 0
        for i in range(self.psize):
            ind = MapIndividual(mutation_rate=self.mutation_rate, map_size=map_size)
            attempts = 1
            max_attempts = 10
            if (playable_count < playable_minimum):
                while(not ind.is_playable()):
                    attempts += 1
                    ind = MapIndividual(mutation_rate=self.mutation_rate, map_size=map_size)
                    if (attempts > max_attempts):
                        ind.force_playable()
                        break
                playable_count += 1
            population.append(ind)
        return population

    def crossover(self, parent1, parent2):
        # Start cloning parents
        child1 = MapIndividual(matrix=parent1.matrix, mutation_rate=self.mutation_rate)
        child2 = MapIndividual(matrix=parent2.matrix, mutation_rate=self.mutation_rate)
        # Then, pick random cell to divide map in four regions
        divider = [parent1.width//2, parent1.height//2]
        center_square_side = 2
        divider[0] += randint(-center_square_side, center_square_side)
        divider[1] += randint(-center_square_side, center_square_side)
        # Swap regions 1 and 4, and leave 2 and 3 equal
        for i in range(divider[0]):
            for j in range(divider[1]):
                child1.matrix[i][j] = parent2.matrix[i][j]
                child2.matrix[i][j] = parent1.matrix[i][j]
        for i in range(divider[0], parent1.width):
            for j in range(divider[1], parent1.height):
                child1.matrix[i][j] = parent2.matrix[i][j]
                child2.matrix[i][j] = parent1.matrix[i][j]
        return child1, child2, divider

    def sort_population(self):
        self.population = sorted(self.population,
                                    key=lambda individual: individual.get_fitness(),
                                    reverse=True)

    def evolve(self):
        for iteration in range(self.iterations):
            # Sort population in descending order by fitness
            self.sort_population()
            if (DEBUG == True and iteration % DEBUG_ITERATION == 0):
                print("##################################")
                best_id = self.population[0].id
                print("Iteration %d" % iteration)
                for i in range(1):
                    print("population[%d]:" % (i))
                    print(self.population[i])

            # Get fitness buffer to avoid heavy cpu load
            ind_fitnesses = []
            total_fitness = 0.0
            for i in self.population:
                cif = i.get_fitness() # Current ind fitness
                ind_fitnesses.append(cif)
                total_fitness += cif
            
            # Creates a pool of individuals such that the higher the
            # fitness, the more replicas an individual has to
            # become a parent.
            parent_pool = []
            pool_max_size = self.psize * 2
            for i in range(len(ind_fitnesses)):
                if (total_fitness > 0.1):
                    ind_weight = ind_fitnesses[i] / total_fitness
                else:
                    ind_weight = 1.0 / self.psize
                ind_replicas = int(ind_weight * pool_max_size)
                for j in range(ind_replicas):
                    parent_pool.append(i)
            if (len(parent_pool) == 0):
                for i in range(len(self.population)):
                    parent_pool.append(i)

            children_start_index = int(self.psize * self.elitism_factor)
            # print("Replacing chidren from %d onward." % (children_start_index))
            for i in range(children_start_index, self.psize - 1, 2):
                # The chance of a parent being chosen depends on its fitness!
                parent1_index = parent_pool[randint(0, len(parent_pool)-1)]
                parent2_index = parent_pool[randint(0, len(parent_pool)-1)]
                limit = 10
                current = 0
                while(parent2_index == parent1_index and current < limit):
                    current += 1
                    parent2_index = parent_pool[randint(0, len(parent_pool)-1)]
                parent1 = self.population[parent1_index]
                parent2 = self.population[parent2_index]
                self.population[i], self.population[i+1], _ = self.crossover(parent1, parent2)

            # Then, mutate everyone with designed probability!
            for ind in self.population:
                ind.mutate()
            
            self.sort_population()

            if (iteration % DEBUG_ITERATION == 0 and DEBUG == True):
                print("At the end of iteration %d, the best individual is:" % iteration)
                for i in range(1):
                    print("population[%d]:" % (i))
                    print(self.population[i])
                
                # k = 0
                # for i in self.population:
                #     if i.id == best_id:
                #         print("The old best id is at position %d and its info is:" % (k))
                #         print(i)
                #     k += 1
    
    def save_best_individuals(self, filename = "gamap", n = 5):
        if not os.path.isdir(os.getcwd() + "/layouts"):
            os.mkdir("layouts")
        for i in range(n):
            f = os.getcwd() + "/layouts/" + filename + str(i) + ".lay"
            with open(f, "w") as mapfile:
                ms = string.replace(self.population[i].parse_map(), tiles_dict["food"], tiles_dict["pacman"], 1)
                mapfile.write(ms)

                
class MazeCell():
    def __init__(self, tile, pos = (0, 0)):
        self.pos = pos
        self.tile = tile
    
    def is_food(self):
        return (self.tile == tiles_dict["food"])
    
    def is_walkable(self):
        if self.tile in [tiles_dict["wall"]]:
            return False
        return True

import time

if __name__ == "__main__":
    st = time.time()
    ga = GeneticAlgorithm(  iterations=100,
                            mutation_rate=0.01,
                            stop_criteria="playable",
                            population_size=100,
                            playable_minimum=10,
                            map_size=15)
    ga.evolve()
    ga.save_best_individuals()
    et = time.time()
    print("The program took %f seconds to complete." % (et - st))