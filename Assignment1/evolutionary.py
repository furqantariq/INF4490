from util import *
import random
import itertools
from pmx import pmx_pair


def evolutionary(distances, generation, ncities, population_size, nParents,
                 mut_rate, cross_rate):
    
    init_set = []
    init_size = 10
    for x in range(init_size):
        init_set.append(random.sample(range(ncities),ncities))
  
    population = [(tour_distance(p, distances),p) for p in init_set]
    
    for x in range(generation):
#        print("============Generation {0} ===========".format(x))
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
    return path + path[:1], cost


def replacement_strategy(offspring, population, psize, distances):
    offspring_eval = [(tour_distance(p, distances),p) for p in offspring]
    population = population + offspring_eval
    population.sort()
    return population[:psize]
    

def mutate(offspring):
    #swap 2 random position with each other
    for x in offspring:
        a = random.randint(0,len(x)-1)
        b = random.randint(0,len(x)-1)
        x[a], x[b] = x[b], x[a]
   
    return offspring
     

def recombine(parents):
    #Parents should be in Even number
    offspring = []
    while parents:
        a=parents.pop()[1]
        b=parents.pop()[1]
#        cut = random.randint(1,len(a)-1)
        c,d = pmx_pair(a,b)
        offspring.append(c)
        offspring.append(d)
        
    return offspring
         

def select_parents(population, nParents):
    Efx = sum([x for (x,y) in population])
    parents = []
    for (a,b) in itertools.cycle(population):
        if nParents == 0:
            break
        #ProbabilityFPS
        Pfps = 1.0-(a/Efx)
        ab = random.uniform(0,1)
        if ab <= Pfps:
            parents.append((a,b))
            nParents = nParents-1
            
    return parents


if __name__ == "__main__":
    
    #Parameters
    population_size = 100
    no_of_generation = 5000
    no_of_parents = 2
    no_of_cities = 24
    mutation_rate = 50 #mutation rate in percentage
    cross_rate = 100 # recombination rate in percentage
    
    cities, distances = read_input("european_cities.csv", no_of_cities)
    path, cost = evolutionary(distances, no_of_generation, no_of_cities, 
                              population_size, no_of_parents, mutation_rate,
                              cross_rate)
    print("Output",[cities[x] for x in path], cost)


