import numpy as np
import random
from classes import *
from selection_scheme import *
import matplotlib.pyplot as plt

class TSP():
    def __init__(self):
        self.population = []
        self.best_so_far = []
        self.avg_so_far = []
        self.children = []
        self.full_lst = []
        self.filename = "qa194.tsp"

        self.mutation_rate = 0.1
        self.no_generations = 100
        self.no_iteration = 10
        self.population_size = 100
        self.off_size = 50

    def readfile(self):
        self.full_lst = []
        with open(self.filename, "r") as f:
            for i in range(7):
                f.readline()
            for line in f:
                data = line.split()
                if len(data) > 1:
                    temp = node(data)
                    self.full_lst.append(temp)
        return self.full_lst

    def filter_nodes(self, region):
        lst = []
        for y in region:
            mlst = []
            for x in self.full_lst:
                if x.id in y:
                    mlst.append(x)
            lst.append(mlst)
            mlst = []
        return lst

    def generate_population(self):
        for i in range(self.generations):
            random.shuffle(self.node_lst)
            temp = copy.deepcopy(self.node_lst)
            temp = chromosome(temp)
            self.population.append(temp)

    def make_children(self):
        for x in range(self.off_size):
            selected_chromosomes = binary_tournament_selection(self.population, 2, True, False)
            temp = selected_chromosomes[0].crossover(selected_chromosomes[1])
            self.children.append(temp)
        return self.children

    def mutate(self):
        for x in range(len(self.children)):
            if random.random() < self.mutation_rate:
                self.children[x].mutate()

    def survival_of_the_fitest(self):
        self.population = self.population + self.children
        self.children.clear()
        self.population = truncation_selection(self.population, self.population_size, False, False)

        self.best_so_far.append(min([self.population[x].fitness for x in range(len(self.population))]))
        self.avg_so_far.append(sum([self.population[x].fitness for x in range(len(self.population))])/len(self.population))
    
class Kmean():
    def __init__(self, filename, k=3, n=1) -> None:
        self.K = k
        self.N = n
        self.dataset = self.initializePoints(filename)
        self.cluster_lst = self.keepClustering(self.dataset, self.K, self.N, False)
        self.region = []

    def initializePoints(self, filename):
        points = []
        with open(filename, "r") as f:
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
        for x in self.cluster_lst:
            for y in x:
                self.region.append(y)
        return self.region

cluster = Kmean("qa194.tsp")
