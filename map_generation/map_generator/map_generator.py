# Program made by Rafael Pontes

from random import randint

tiles_dict = {
    "food": ".",
    "wall": "%",
    #"P": "pacman",
    #"o": "specialfood",
    #"G": "ghost",
    #" ": "blank"
}
tiles = list(tiles_dict.values())
NUM_TILES = len(tiles)

class MapIndividual():
    def __init__(self, w = 10, h = 10, m = None):
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

    def get_fitness(self):
        return 0
    
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

        # s = ""
        # for row in visited:
        #     for col in row:
        #         col = "F" if col == False else "T"
        #         s += col + " "
        #     s += "\n"
        # print(s)

        # Check if all are visited
        for i in range(len(visited)):
            for j in range(len(visited[0])):
                if (visited[i][j] == False):
                    # There's at least one unreachabled cell
                    return False
        return True


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

individuals = [] # Each map generated in the population

if __name__ == "__main__":
    for i in range(1):
        individual = MapIndividual()
        while(not individual.is_playable()):
            individual = MapIndividual()
        individuals.append(individual)
    
    for i in individuals:
        print("==============")
        print(i)
        print("playable? %s" % (str(i.is_playable())))
        print("==============")