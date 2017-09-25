# -*- coding: utf-8 -*-

from util import *
import itertools
import sys

def exhaustive_search(distances, nCities):
    min_d = sys.maxsize
    path = ()
    for p in itertools.permutations(range(nCities)):
#        print(p)
        d = tour_distance(p, distances)
        if d < min_d:
            min_d = d
            path = p
    return path + path[:1], min_d
        
        
if __name__ == "__main__":
    
    #Parameters
    num_of_cities = 6  
    
    cities, distances = read_input("european_cities.csv", num_of_cities)
    path, cost = exhaustive_search(distances, num_of_cities)
    print("Output",[cities[x] for x in path], cost)
