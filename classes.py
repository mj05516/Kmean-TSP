from typing import List
import math
import random
import copy

class node:
    def __init__(self, *args):
        if len(args[0]) == 3:
            self.id = int(args[0][0])
            self.x = float(args[0][1])
            self.y = float(args[0][2])

        elif len(args) == 2:
            self.value = int(args[0])
            self.weight = int(args[1])
            self.added = random.randint(0,1)

        elif len(args[0]) == 4:
            self.id = int(args[0][0])
            self.colorNum = args[0][1]            
            self.neighbours = args[0][2]

        
class chromosome:
    def __init__(self, seq: List[node]= []):
        self.sequence = seq
        self.fitness = 0
        self.age = 0
        self.weight = 0

    def calc_cartisian_dist(self, node1, node2):
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    def calc_fitness_tsp(self):
        self.fitness = 0
        for i in range(len(self.sequence) - 1):
            self.fitness += self.calc_cartisian_dist(self.sequence[i], self.sequence[i+1])

        return self.fitness

    def calc_fitness_knapsack(self):
        self.fitness = 0
        self.weight = 0
        seq = copy.deepcopy(self.sequence)
        for i in range(len(seq)):
            if seq[i].added == 1:
                self.fitness += seq[i].value
                self.weight += seq[i].weight
            if self.weight > 878:
                self.fitness = 0
                return 0
        return self.fitness

    def calc_fitness_graph_coloring(self, edges):
        self.fitness = 0
        for x in copy.deepcopy(self.sequence):
            color = x.colorNum
            for y in x.neighbours:
                if self.sequence[int(y)-1].colorNum == color:
                    self.fitness += 1
        return self.fitness


    def crossover(self, other):
        assert isinstance(other, chromosome)
        seq1 = copy.deepcopy(self.sequence)
        seq2 = copy.deepcopy(other.sequence)
        bound1 = random.randint(0, len(seq1)//2)
        bound2 = random.randint(bound1, len(seq1)-1)
        child = ['-']*len(seq1)

        for x in range(bound1, bound2+1):
            child[x] = seq1[x]

        for x in range(bound2+1, len(child)):
            if seq2[x] not in child:
                child[x] = seq2[x]
            else:
                i = x
                while seq2[i] in child and '-' in child:
                    i = (i+1)%len(child)
                child[x] = seq2[i]

        for x in range(bound1):
            if seq2[x] not in child:
                child[x] = seq2[x]
            else:
                i = x
                while seq2[i] in child and '-' in child:
                    i = (i+1)%len(child)
                child[x] = seq2[i]

        return chromosome(child)
        

    def mutate(self):
        node1 = random.randint(0, len(self.sequence)-1)
        node2 = random.randint(0, len(self.sequence)-1)
        self.sequence[node1], self.sequence[node2] = self.sequence[node2], self.sequence[node1]
        return

    def mutate_knapsack(self):
        node1 = random.randint(0, len(self.sequence)-1)
        node2 = random.randint(0, len(self.sequence)-1)
        self.sequence[node1].added = (self.sequence[node1].added + 1)%2
        self.sequence[node2].added = (self.sequence[node2].added + 1)%2
        return

    def mutate_graph_coloring(self):
        node1 = random.randint(0, len(self.sequence)-1)
        node2 = random.randint(0, len(self.sequence)-1)
        self.sequence[node1].colorNum, self.sequence[node2].colorNum = self.sequence[node2].colorNum, self.sequence[node1].colorNum
        return

    def get_sequence(self):
        temp = []
        for x in self.sequence:
            temp.append(x.id)
        return temp