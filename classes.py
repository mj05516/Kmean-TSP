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

class chromosome:
    def __init__(self, seq: List[node]= []):
        self.sequence = seq
        self.fitness = 0
        self.calc_fitness_tsp()

    def calc_fitness_tsp(self):
        fitness = 0
        seq = copy.deepcopy(self.sequence)
        for i in range(len(seq) - 1):
            fitness += math.sqrt((seq[i].x - seq[i+1].x)**2 + (seq[i].y - seq[i+1].y)**2)
        
        self.fitness = fitness
        return fitness

    def crossover(self, other):
        assert isinstance(other, chromosome)
        seq1 = copy.deepcopy(self.sequence)
        seq2 = copy.deepcopy(other.sequence)
        bound1 = random.randint(0, len(seq1)//2)
        bound2 = random.randint(bound1, len(seq1)-1)
        child = [0]*len(seq1)
        done = []

        for x in range(bound1, bound2+1):
            child[x] = seq1[x]
            done.append(seq1[x].id)

        # print("after seq 1:")
        # for x in child:
        #     print(x.id, end=" ")
        # print()

        for x in range(bound2+1, len(child)):
            if seq2[x].id not in done:
                child[x] = seq2[x]
                done.append(seq2[x].id)
            else:
                i = x
                while seq2[i].id in done:
                    i = (i+1)%len(child)
                child[x] = seq2[i]
                done.append(seq2[i].id)

        for x in range(bound1):
            if seq2[x].id not in done:
                child[x] = seq2[x]
                done.append(seq2[x].id)
            else:
                i = x
                while seq2[i].id in done:
                    i = (i+1)%len(child)
                child[x] = seq2[i]
                done.append(seq2[i].id)

        return chromosome(child)

    def mutate(self):
        node1 = random.randint(0, len(self.sequence)-1)
        node2 = random.randint(0, len(self.sequence)-1)
        self.sequence[node1], self.sequence[node2] = self.sequence[node2], self.sequence[node1]
        return

    def get_sequence(self):
        temp = []
        for x in self.sequence:
            temp.append(x.id)
        return temp