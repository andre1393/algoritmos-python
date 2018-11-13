import numpy as np
import pandas as pd

def evaluate(population):
    ev = []
    for i in population:
        ev.append(sum(i))
    
    return ev

class GA:
    
    def __init__(self, max_gen = 100, n_individuals = 10, n_chrom = 4, replace = False, p_crossover = 0.5, p_mutation = 0.005):
        self.max_gen = max_gen
        self.n_individuals = n_individuals
        self.n_chrom = n_chrom
        self.replace = replace
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation

    # todo: transformar tudo em np.array
    def initialize(self):
        init = []
        for i in range(self.n_individuals):
            init.append(np.random.choice(self.gene, replace = self.replace, size = self.n_chrom))
        
        self.population = init
        print('populacao inicial: ', self.population)
    def crossover(self):
        new_generation = []
        half = self.n_chrom/2
        for i in range(0, len(self.population), 2):
            if np.random.uniform() < self.p_crossover: # crossover 
                n1 = np.concatenate((self.population[i][0:half], self.population[i + 1][half:]), axis = 0)
                n2 = np.concatenate((self.population[i][half:], self.population[i + 1][0:half]), axis = 0)
                new_generation.append(n1)
                new_generation.append(n2)
            else:
                new_generation.append(self.population[i])
                new_generation.append(self.population[i+1])
        
        self.population = new_generation

    def mutate(self):
        mutated_population = []
        for i in self.population:
            if(np.random.uniform() < self.p_mutation):
                mutated_chrom = np.random.choice(self.gene)
                i[np.random.randint(len(i))] = mutated_chrom
                mutated_population.append(i)
            else:
                mutated_population.append(i)
                
        self.population = mutated_population

    def select(self, ev, elitism = True):
        self.population = self.gen_choice(self.population, p = ev/sum(ev), size = len(self.population), elitism = elitism)
    
    def gen_choice(self, population, p, size, elitism):

        best = -np.inf
        best_i = None
        idx = np.random.choice(range(len(population)), p = p, size = size)
        selected_population = []
        for i in idx:
            if p[i] >= best:
                best_i = self.population[i]
            selected_population.append(self.population[i])
        
        selected_population[0] = best_i
        
        print(sum(best_i))
        return selected_population
        
    def fit(self, evaluate, gene):
        self.evaluate = evaluate
        self.gene = gene
        
        self.initialize()

        for i in range(self.max_gen):
            self.crossover()
            self.mutate()
            ev = evaluate(self.population)
            self.select(ev)

        return self.population 

model = GA(max_gen = 1000, replace = True)
model.fit(evaluate, [0, 1, 2, 3, 4, 5])