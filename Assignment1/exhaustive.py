# -*- coding: utf-8 -*-

from util import *
import itertools
import sys
import time

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
    num_of_cities = 24

    cities, distances = read_input("european_cities.csv", num_of_cities)

    start_time = time.time()
    path, cost = exhaustive_search(distances, num_of_cities)
    time_taken = time.time()-start_time
    print(" %s seconds " % time_taken)

    print(" --- Output --- ")
    print([cities[x] for x in path], cost)
