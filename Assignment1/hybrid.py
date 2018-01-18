from lamarckian import *
from baldwinian import *
import time
import numpy as np
import matplotlib.pyplot as plt
from util import *


if __name__ == "__main__":

    #Parameters
    population_size = 50
    no_of_generation = 100
    no_of_parents = 10
    no_of_cities = 10
    mutation_rate = 50 #mutation rate in percentage
    cross_rate = 100 # recombination rate in percentage
    learning_iteration = 5

    no_of_runs = 20

    cities, distances = read_input("european_cities.csv", no_of_cities)

    file = open("out_{0}_cities_lamarckian.txt".format(no_of_cities), "w")

    gen_fits = np.zeros(no_of_generation)
    
    for x in range(no_of_runs):
        start_time = time.time()
        path, cost, best_fits = lamarckian(distances, no_of_generation, no_of_cities,
                                population_size, no_of_parents, mutation_rate,
                                cross_rate, learning_iteration)
        time_taken = time.time() - start_time
        file.write("{0};{1};{2};{3};\n".format(x, [cities[x] for x in path], cost, time_taken ))
        print("%s Seconds " % time_taken)
        print("--Output--")
        print([cities[x] for x in path], cost)
        gen_fits = np.add(gen_fits, np.array(best_fits))

    file.close()

    gen_fits = gen_fits / no_of_runs
    x = np.linspace(0,no_of_generation,num=no_of_generation)
    plt.plot(x, gen_fits,label="Lamarckian")

    file = open("out_{0}_cities_baldwinian.txt".format(no_of_cities), "w")
    
    gen_fits = np.zeros(no_of_generation)
    
    for x in range(no_of_runs):
        start_time = time.time()
        path, cost, best_fits = baldwinian(distances, no_of_generation, no_of_cities,
                                population_size, no_of_parents, mutation_rate,
                                cross_rate, learning_iteration)
        time_taken = time.time() - start_time
        file.write("{0};{1};{2};{3};\n".format(x, [cities[x] for x in path], cost, time_taken ))
        print("%s Seconds " % time_taken)
        print("--Output--")
        print([cities[x] for x in path], cost)
        gen_fits = np.add(gen_fits, np.array(best_fits))

    file.close()
    
    gen_fits = gen_fits / no_of_runs
    x = np.linspace(0,no_of_generation,num=no_of_generation)
    plt.plot(x, gen_fits,label="Baldwinian")

    plt.title("Hybrid Algorithms")
    plt.xlabel("No. of Generations")
    plt.ylabel("Average Fitness")   
    plt.legend()
    plt.savefig("hybrid.png", format="png", dpi=1000)       
  