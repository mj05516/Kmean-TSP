import numpy as np
import random
from classes import *
from selection_scheme import *
import matplotlib.pyplot as plt
from itertools import permutations
from tqdm import tqdm

class TSP():
    def __init__(self, filename):
        self.population = []
        self.best_so_far = []
        self.bestpath = node([-2,-2,-2])
        self.avg_so_far = []
        self.children = []
        self.node_lst = []
        self.filename = filename

        self.mutation_rate = 0.7
        self.no_generations = 1000
        self.no_iteration = 1
        self.population_size = 100
        self.off_size = 75

    def generate_population(self):
        for i in range(self.no_generations):
            random.shuffle(self.node_lst)
            temp = copy.deepcopy(self.node_lst)
            temp = chromosome(temp)
            self.population.append(temp)

    def make_children(self):
        for x in range(self.off_size):
            selected_chromosomes = binary_tournament_selection(self.population, 2, True, False)
            temp = selected_chromosomes[0].crossover(selected_chromosomes[1])
            self.children.append(temp)

    def mutate(self):
        for x in range(len(self.children)):
            if random.random() < self.mutation_rate:
                self.children[x].mutate()

    def survival_of_the_fitest(self):
        self.population = self.population + self.children
        self.children.clear()
        self.population = truncation_selection(self.population, self.population_size, False, False)
        
        # sort population by fitness
        self.population.sort(key=lambda x: x.fitness)

        self.best_so_far.append(self.population[0].fitness)
        self.bestpath = self.population[0]
        self.avg_so_far.append(sum([self.population[x].fitness for x in range(len(self.population))])/len(self.population))
    
class Kmean():
    def __init__(self, filename, k=3, n=10) -> None:
        self.K = k
        self.N = n
        self.filename = filename
        self.dataset = self.initializePoints()
        self.cluster_lst = self.keepClustering(self.dataset, self.K, self.N, False)
        self.dict = self.makeDic()
        self.region = self.cord_to_region()
        

    def initializePoints(self, ):
        points = []
        with open(self.filename, "r") as f:
            for i in range(7):
                f.readline()
            for line in f:
                data = line.split()
                data = [float(x) for x in data[1:]]
                points.append(data)
        return points[:-1]

    def point_clustering(self, points, centroids):
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

    def visualize(self, clustered_data, Iteration):
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

    def mean_center(self, centroids):
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
                self.visualize(centroids, 404)
        return new_centers

    def cluster(self, points,K,visuals = True):
        clusters=[]
        data_cluster = self.point_clustering(points, self.make_random_center(points, K))
        prev_cntr = data_cluster
        iteration = 0
        while(True):
            new_cntr = self.mean_center(data_cluster)
            data_cluster =  self.point_clustering(points, new_cntr)
            if visuals: 
                self.visualize(data_cluster, iteration)

            if prev_cntr.keys() == new_cntr.keys():
                break
            else:
                prev_cntr = data_cluster
            iteration += 1
        
        return data_cluster

    def make_random_center(self, points, k):
        centroids = {}
        lst = random.sample(points, k)
        for x in lst:
            centroids[(x[0],x[1])] = []
        return centroids

    def clusterQuality(self, clusters):
        score = -1
        for x in clusters.keys():
            for y in clusters[x]:
                score += (x[0] - y[0])**2 + (x[1] - y[1])**2

        return score

    def keepClustering(self, points,K,N,visuals):
        clusters = []
        lst = []
        min = 999**999
        for x in range(N):
            print("Iteration No.: ", x+1, "/", N)
            data_cluster = self.cluster(points,K,visuals)
            score = self.clusterQuality(data_cluster)
            print("Score: ", score,"\n")
            if score < min:
                min = score
                clusters = ([data_cluster, min, x+1])

        for x in clusters[0].keys():
            lst.append(clusters[0][x])
        return lst

    def makeDic(self):
        dic = {}
        with open(self.filename, "r") as f:
            for i in range(7):
                f.readline()
            for line in f:
                data = line.split()
                if len(data) > 1:
                    dic[float(data[1]),float(data[2])] = int(data[0])
        return dic
    
    def cord_to_region(self):
        region = []
        lst = []
        for i in self.cluster_lst:
            for j in i:
                lst.append(self.dict[j[0],j[1]])
            region.append(lst)
            lst = []
        return region



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

def filter_nodes(node_lst, region):
    lst = []
    for y in region:
        mlst = []
        for x in node_lst:
            if x.id in y:
                mlst.append(x)
        lst.append(mlst)
        mlst = []
    return lst

def main():
    cluster = Kmean("qa194.tsp")

    filter_lst = []
    node_lst = readfile("qa194.tsp")    
    filter_lst = filter_nodes(node_lst, cluster.region)

    tsp1 = TSP("qa194.tsp")
    tsp2 = TSP("qa194.tsp")
    tsp3 = TSP("qa194.tsp")

    tsp1.node_lst = filter_lst[0]
    tsp2.node_lst = filter_lst[1]
    tsp3.node_lst = filter_lst[2]

    tsp1.generate_population()
    tsp2.generate_population()
    tsp3.generate_population()

    for i in tqdm(range(tsp1.no_generations)):
        tsp1.make_children()
        tsp1.mutate()
        tsp1.survival_of_the_fitest()
        if i % 100 == 0:
            print("TSP1: Generation No.: ", i+1)
            print("Best Fitness Soo Far: ", tsp1.best_so_far[-1])
        # add loading bar for this loop


    for i in tqdm(range(tsp2.no_generations)):
        tsp2.make_children()
        tsp2.mutate()
        tsp2.survival_of_the_fitest()
        if i % 100 == 0:
            print("TSP2: Generation No.: ", i+1)
            print("Best Fitness Soo Far: ", tsp2.best_so_far[-1])

    for i in tqdm(range(tsp3.no_generations)):
        tsp3.make_children()
        tsp3.mutate()
        tsp3.survival_of_the_fitest()
        if i % 100 == 0:
            print("TSP3: Generation: ", i+1)
            print("Best Fitness Soo Far: ", tsp3.best_so_far[-1])

    final = TSP("qa194.tsp")
    lst = []
    lst.append(tsp1.bestpath.sequence)
    lst.append(tsp2.bestpath.sequence)
    lst.append(tsp3.bestpath.sequence)

    final.node_lst = tsp1.bestpath.sequence +tsp2.bestpath.sequence + tsp3.bestpath.sequence
    perm = list(permutations(lst))
    for x in perm:
        temp = []
        for y in x:
            temp += y
        final.population.append(chromosome(temp))
        temp = []

    for i in tqdm(range(final.no_generations)):
        final.make_children()
        final.mutate()
        final.survival_of_the_fitest()
        if i % 100 == 0:
            print("Final: Generation: ", i+1)
            print("Best Fitness Soo Far: ", final.bestpath.fitness)


    # for i in tsp1.bestpath.sequence:
    #     plt.scatter(i.x, i.y, color='red')
    # for i in tsp2.bestpath.sequence:
    #     plt.scatter(i.x, i.y, color='blue')
    # for i in tsp3.bestpath.sequence:
    #     plt.scatter(i.x, i.y, color='green')

    # # connect the dots in the best path
    # for i in range(len(tsp1.bestpath.sequence)-1):
    #     plt.plot([tsp1.bestpath.sequence[i].x, tsp1.bestpath.sequence[i+1].x], [tsp1.bestpath.sequence[i].y, tsp1.bestpath.sequence[i+1].y], color='red')
    # for i in range(len(tsp2.bestpath.sequence)-1):
    #     plt.plot([tsp2.bestpath.sequence[i].x, tsp2.bestpath.sequence[i+1].x], [tsp2.bestpath.sequence[i].y, tsp2.bestpath.sequence[i+1].y], color='blue')
    # for i in range(len(tsp3.bestpath.sequence)-1):
    #     plt.plot([tsp3.bestpath.sequence[i].x, tsp3.bestpath.sequence[i+1].x], [tsp3.bestpath.sequence[i].y, tsp3.bestpath.sequence[i+1].y], color='green')

    # plt.show()

if __name__ == "__main__":
    main()