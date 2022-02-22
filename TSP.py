from itertools import count
from classes import *
from selection_scheme import *
import numpy as np
import matplotlib.pyplot as plt

def initializePoints(filename):
    points = []
    with open(filename, "r") as f:
        for i in range(7):
            f.readline()
        for line in f:
            data = line.split()
            data = [float(x) for x in data[1:]]
            # print(data)
            # data[0] = int(data[0])
            # data = data[1:]+data[0]
            points.append(data)
    return points[:-1]

def make_random_center(points, k):
    centroids = {}
    lst = random.sample(points, k)
    for x in lst:
        centroids[(x[0],x[1])] = []
    return centroids


def point_clustering(points, centroids):
    for point in points:
        nearest_dist_from_ref = 999**999
        centro_point = None
        for i in centroids.keys():
            euclidean_dist = np.linalg.norm(np.subtract(list(i),list(point)))
            if euclidean_dist < nearest_dist_from_ref:
                nearest_dist_from_ref = euclidean_dist
                centro_point = i
        centroids[centro_point].append(point)
    return centroids


def mean_center(centroids):
    new_centers = {}
    for x in centroids.keys():
        array = np.array(centroids[x])
        np.shape(array)
        try:
            xcord,ycord = np.mean(array[:,0]), np.mean(array[:,1])
            gravity_center = (xcord,ycord)
            new_centers[gravity_center] = []
        except:
            gravity_center = x
            new_centers[gravity_center] = []
            visualize(centroids, 404)
    return new_centers


def clusterQuality(clusters):
    score = -1
    for x in clusters.keys():
        for y in clusters[x]:
            score += (x[0] - y[0])**2 + (x[1] - y[1])**2

    return score


def cluster(points,K,visuals = True):
    clusters=[]
    data_cluster = point_clustering(points, make_random_center(points, K))
    prev_cntr = data_cluster
    iteration = 0
    while(True):
        new_cntr = mean_center(data_cluster)
        data_cluster =  point_clustering(points, new_cntr)
        if visuals: 
            visualize(data_cluster, iteration)

        if prev_cntr.keys() == new_cntr.keys():
            break
        else:
            prev_cntr = data_cluster
        iteration += 1
    
    return data_cluster


def visualize(clustered_data, Iteration):
    plotx = []
    ploty = []
    clr = ["cyan","magenta","green", "red", "yellow", "blue"]

    for x in clustered_data.keys():
        try:
            array = np.array(clustered_data[x])
            plotx,ploty = array[:,0], array[:,1]
            plt.plot(plotx,ploty, '+', color=clr.pop())
        except:
            pass

    for x in clustered_data.keys():
        plt.plot(x[0], x[1], 'o' ,color='black')

    plt.title("Iteration: " + str(Iteration))
    plt.show()


def keepClustering(points,K,N,visuals):
    clusters = []
    min = 999**999
    for x in range(N):
        print("Iteration No.: ", x+1, "/", N)
        data_cluster = cluster(points,K,visuals)
        score = clusterQuality(data_cluster)
        print("Score: ", score,"\n")
        if score < min:
            min = score
            clusters = ([data_cluster, min, x+1])
    return clusters


def cluster_to_region(cluster, dict):
    region = []
    for i in cluster:
        region.append(dict[i[0],i[1]])
    return region

def makedic(filename):
    dic = {}
    with open(filename, "r") as f:
        for i in range(7):
            f.readline()
        for line in f:
            data = line.split()
            if len(data) > 1:
                dic[float(data[1]),float(data[2])] = int(data[0])
    return dic
    
def readfile(filename):
    node_lst = []
    with open(filename, "r") as f:
        for i in range(7):
            f.readline()
        for line in f:
            data = line.split()
            if len(data) > 1:
                temp = node(data)
                node_lst.append(temp)
    return node_lst

def TSP_EA(node_lst, pop_size, off_size, no_generations, mut_rate, no_iteration):
    best_per_iter = []
    avg_per_iter = []

    for j in range(no_iteration):
        population = []
        best_so_far = []
        avg_so_far = []

        for i in range(pop_size):
            random.shuffle(node_lst)
            temp = chromosome(node_lst.copy())
            temp.calc_fitness_tsp()
            population.append(temp)
        
        for i in range(no_generations):
            children = []
            for x in range(off_size):
                selected_chromosomes = truncation_selection(population, 2, True, False)
                children.append(selected_chromosomes[0].crossover(selected_chromosomes[1]))

            for x in range(off_size):
                if random.random() < mut_rate:
                    children[x].mutate()

            for x in children:
                x.fitness = x.calc_fitness_tsp()
                population.append(x)
        
            population = random_selection(population, pop_size, False)

            best_so_far.append(min([population[x].fitness for x in range(len(population))]))
            avg_so_far.append(sum([population[x].fitness for x in range(len(population))])/len(population))

            if i % 100 == 0:
                print("Iteration: {}, Generation: {}".format(j, i))
                print("Best fitness: {}".format(population[0].fitness))

        best_per_iter.append(best_so_far)
        avg_per_iter.append(avg_so_far)

    Avg_BFS_pg = [sum([k[i] for k in best_per_iter])/no_iteration for i in range(no_generations)]
    Avg_avgfit_pg = [sum([k[i] for k in avg_per_iter])/no_iteration for i in range(no_generations)]
    
    plt.figure(figsize=(10,6))
    plt.plot(range(no_generations),Avg_BFS_pg, label="Best Fitness")
    plt.plot(range(no_generations),Avg_avgfit_pg, label="Average Fitness")
    plt.xlabel("Number of Generations")
    plt.ylabel("Average Value per generations\n Lower is better")
    plt.title("TSP EA:\n Truncation Selection and Random Selection")
    plt.legend()
    plt.show()
    return 

def filter_nodes(node_lst, region):
    lst = []
    for y in range(len(region)):
        mlst = []
        for x in node_lst:
            if x.id in region:
                mlst.append(x)
        lst.append(mlst)
        mlst = []
    return lst


def main():
    K = 3
    N = 5
    count = 0
    cluster_lst = ['*']*K
    region_node_lst = []
    points = initializePoints('qa194.tsp')
    clusters = keepClustering(points, K, N, False)
    for x in clusters[0].keys():
        cluster_lst[count] = clusters[0][x]
        count += 1
    
    dict = makedic("qa194.tsp")
    for x in range(len(cluster_lst)):
        region_node_lst.append(cluster_to_region(cluster_lst[x], dict))

    node_lst = readfile("qa194.tsp")
    filter_lst = filter_nodes(node_lst, region_node_lst[0])
    pop_size = 100
    off_size = 50
    no_generations = 1000
    mut_rate = 0.3
    no_iteration = 1
    TSP_EA(filter_lst[0], pop_size, off_size, no_generations, mut_rate, no_iteration)
    TSP_EA(filter_lst[1], pop_size, off_size, no_generations, mut_rate, no_iteration)
    TSP_EA(filter_lst[2], pop_size, off_size, no_generations, mut_rate, no_iteration)

if __name__ == "__main__":
    main()