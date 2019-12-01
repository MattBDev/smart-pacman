# Program made by Rafael Pontes

from random import randint

tiles_dict = {
    ".": "food",
    "%": "wall",
    "P": "pacman",
    "o": "specialfood",
    "G": "ghost",
    " ": "blank"
}
tiles = list(tiles_dict.keys())
NUM_TILES = len(tiles)

class MapIndividual():
    def __init__(self, w = 10, h = 10, m = None):
        super().__init__()
        self.width = w
        self.height = h
        if (m == None):
            self.generate_random_map()
        else:
            self.matrix = m

    def __str__(self):
        s = ""
        for row in self.matrix:
            for col in row:
                s += col + " "
            s += "\n"
        return s
        
    def generate_random_map(self):
        self.matrix = []
        for i in range(self.width):
            self.matrix.append(list())
            for j in range(self.height):
                index = randint(0, NUM_TILES - 1)
                self.matrix[i].append(tiles[index])
        save_map(self.matrix)

individuals = [] # Each map generated in the population

def save_map(map_matrix):
    individuals.append(map_matrix)

if __name__ == "__main__":
    for i in range(10):
        individual = MapIndividual()
        individuals.append(individual)
    
    for i in individuals:
        print(i)