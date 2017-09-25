import csv
 
def read_input(filename, nCities):
    data = list(csv.reader(open(filename),delimiter=';'))
    return data[0][:nCities], [i[:nCities] for i in data[1:nCities+1]]


def tour_distance(perm, distances): 
    shift = perm[1:] + perm[:1]
    value = [float(distances[i][j]) for i,j in zip(perm, shift)]
    return sum(value) 