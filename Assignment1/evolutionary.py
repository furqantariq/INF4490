from util import *
import random
import itertools
from pmx import pmx_pair
import time
import numpy as np
import matplotlib.pyplot as plt


def evolutionary(distances, generation, ncities, population_size, nParents,
                 mut_rate, cross_rate):

    init_set = []
    init_size = 10
    for x in range(init_size):
        init_set.append(random.sample(range(ncities),ncities))

    population = [(tour_distance(p, distances),p) for p in init_set]

#   For plotting
    best_fit = []

    for x in range(generation):
#        print("============Generation {0} ===========".format(x))
        parents = select_parents(population, nParents)

        offspring = []
        if random.randint(0,100) <= cross_rate:
            offspring = recombine(parents)

        if random.randint(0,100) <= mut_rate:
            offspring = mutate(offspring)

        population = replacement_strategy(offspring, population, population_size, distances)
        best_fit.append(population[0][0])

    cost,path = population[0]
    return path + path[:1], cost, best_fit


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
    no_of_generation = 1000
    no_of_parents = 10
    no_of_cities = 24
    mutation_rate = 50 #mutation rate in percentage
    cross_rate = 100 # recombination rate in percentage

    no_of_runs = 20

    cities, distances = read_input("european_cities.csv", no_of_cities)

    for pop_size in [50, 200, 400]:
        
        population_size = pop_size
        file = open("out_{0}_cities_evolutionary{1}.txt".format(no_of_cities,pop_size), "w")
        
        gen_fits = np.zeros(no_of_generation)
        
        for x in range(no_of_runs):
            start_time = time.time()
            path, cost, best_fits = evolutionary(distances, no_of_generation, no_of_cities,
                                    population_size, no_of_parents, mutation_rate,
                                    cross_rate)
            time_taken = time.time() - start_time
            file.write("{0};{1};{2};{3};\n".format(x, [cities[x] for x in path], cost, time_taken ))        
            print("%s Seconds " % time_taken)
            print("--Output--")
            print([cities[x] for x in path], cost)
            gen_fits = np.add(gen_fits, np.array(best_fits))
            
         
        gen_fits = gen_fits / no_of_runs
        x = np.linspace(0,no_of_generation,num=no_of_generation)
        plt.plot(x, gen_fits,label="Population size {0}".format(pop_size))

    plt.title("Evolutionary Algorithms")
    plt.xlabel("No. of Generations")
    plt.ylabel("Average Fitness")   
    plt.legend()
    plt.savefig("evolutionary.png", format="png", dpi=1000)       
        

    file.close()
