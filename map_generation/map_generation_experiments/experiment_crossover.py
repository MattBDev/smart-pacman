from map_generator import *

ga = GeneticAlgorithm()
alice = MapIndividual()
bob = MapIndividual()
print("Alice: %s" % (alice))
print("Bob: %s" % (bob))
child1, child2, divider = ga.crossover(alice, bob)
print("\nThe crossover from Alice and Bob led to these children:")
print("Child 1: %s" % (child1))
print("Child 2: %s" % (child2))
print("Divider was this point: %s" % (divider))