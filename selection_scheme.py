from select import select
from classes import *
from classes import chromosome

lst: chromosome = []

def truncation_selection(population, popsize, pre_selection: bool = True, max_prob = True):
    if max_prob:
        population.sort(key=lambda x: x.fitness, reverse=True)
    else:
        population.sort(key=lambda x: x.fitness)

    if pre_selection:    
        return population[:2]
    else:
        return population[:popsize]

def random_selection(population, popsize, pre_selection: bool = True):
    selected = []
    if pre_selection:
        for x in range(2):
            selected.append(random.choice(population))
    else:
        for x in range(popsize):
            selected.append(random.choice(population))
    return selected
    
def fitness_proportionate_selection(population , popsize, pre_selection: bool = True, max_prob = True):
    total_fitness = sum(x.fitness for x in population)
    if pre_selection:
        if max_prob:
            selection_prob = [x.fitness/total_fitness for x in population]
            return random.choices(population, weights=selection_prob, k=2)
        else:
            selection_prob = [1 - x.fitness/total_fitness for x in population]
            return random.choices(population, weights=selection_prob, k=2)
    else:
        if max_prob:
            selection_prob = [x.fitness/total_fitness for x in population]
            return random.choices(population, weights=selection_prob, k=popsize)
        else:
            selection_prob = [1 - x.fitness/total_fitness for x in population]
            return random.choices(population, weights=selection_prob, k=popsize)

def binary_tournament_selection(population, popsize, pre_selection: bool = True, max_prob = True):
    tournament_size = 2
    random_chromosomes = []
    selected_chromosomes = []
    if pre_selection:
        for x in range(2):
            for x in range(tournament_size):
                random_chromosomes.append(random.choice(population))
            if max_prob:
                random_chromosomes.sort(key=lambda x: x.fitness, reverse=True)
            else:
                random_chromosomes.sort(key=lambda x: x.fitness)
            selected_chromosomes.append(random_chromosomes[0])
    else:
        for x in range(popsize):
            for x in range(tournament_size):
                random_chromosomes.append(random.choice(population))
            if max_prob:
                random_chromosomes.sort(key=lambda x: x.fitness, reverse=True)
            else:
                random_chromosomes.sort(key=lambda x: x.fitness)
            selected_chromosomes.append(random_chromosomes[0])
    return selected_chromosomes

def rank_based_selection(population, popsize, pre_selection: bool = True, max_prob = True):
    if pre_selection:
        if max_prob:
            population.sort(key=lambda x: x.fitness, reverse=True)
            t_ranks = sum(x for x in range(len(population)))
            selection_prob = [x/t_ranks for x in range(len(population))]
            return random.choices(population, weights=selection_prob, k=2)
        else:
            population.sort(key=lambda x: x.fitness)
            t_ranks = sum(x for x in range(len(population)))
            selection_prob = [1 - x/t_ranks for x in range(len(population))]
            return random.choices(population, weights=selection_prob, k=2)

    else:
        if max_prob:
            population.sort(key=lambda x: x.fitness, reverse=True)
            t_ranks = sum(x for x in range(len(population)))
            selection_prob = [x/t_ranks for x in range(len(population))]
            return random.choices(population, weights=selection_prob, k=popsize)
        else:
            population.sort(key=lambda x: x.fitness)
            t_ranks = sum(x for x in range(len(population)))
            selection_prob = [1 - x/t_ranks for x in range(len(population))]
            return random.choices(population, weights=selection_prob, k=popsize)