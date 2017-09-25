from util import *
from hillclimbng import hillclimb
from evolutionary import *
import random


def baldwinian(distances, generation, ncities, population_size, nParents,
                 mut_rate, cross_rate, learning_iteration):
    
    init_set = []
    init_size = 10
    for x in range(init_size):
        init_set.append(random.sample(range(ncities),ncities))
  
    population = [(tour_distance(p, distances),p) for p in init_set]
    
    for x in range(generation):
        print("============Generation {0} ===========".format(x))
        
        population = baldwinian_learning(population, learning_iteration, distances)

        parents = select_parents(population, nParents)
#       print(parents)
        
        offspring = []
        if random.randint(0,100) <= cross_rate:
            offspring = recombine(parents)
#            print("crossed",offspring)
        
        if random.randint(0,100) <= mut_rate:
            offspring = mutate(offspring)
 #           print("mutated",offspring)
        
        population = replacement_strategy(offspring, population, population_size, distances)
#        print(population)
        
    cost,path = population[0]
    return path + path[:1], tour_distance(path, distances)

def baldwinian_learning(pop, n, distances):
    for i, (a,b) in enumerate(pop):
        for x in range(n):
            (c,d) = hillclimb(b,a,distances)
        pop[i] = (c,b) # Only updating fitness not actual genotype
    return pop


if __name__ == "__main__":
    
    #Parameters
    population_size = 100
    no_of_generation = 100
    no_of_parents = 6
    no_of_cities = 24
    mutation_rate = 50 #mutation rate in percentage
    cross_rate = 100 # recombination rate in percentage
    learning_iteration = 10
    
    cities, distances = read_input("european_cities.csv", no_of_cities)
    path, cost = baldwinian(distances, no_of_generation, no_of_cities, 
                              population_size, no_of_parents, mutation_rate,
                              cross_rate, learning_iteration)
    print("Output",[cities[x] for x in path], cost)