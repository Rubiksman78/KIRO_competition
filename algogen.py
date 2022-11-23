import random
import numpy as np
import sys
import copy 
from functions import *
import wandb

class AlgoGen:
    def __init__(self, dict, solution, pop_size, max_gen, mutation_rate, crossover_rate, elitism_rate):
        self.dict = dict
        self.solution = solution
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.population = []
        self.fitness = []
        self.best_cost = sys.maxsize
        self.best_sol = None
        self.contraint = Constraint(dict)
        self.valid = self.constraint.valid

    def init_population(self):
        for i in range(self.pop_size):
            self.population.append(self.random_sol())

    def random_sol(self):
       pass

    def compute_fitness(self):
        self.fitness = []
        for sol in self.population:
            self.fitness.append(cost(sol, self.dict))

    def tournament_selection(self, k):
        best = None
        for i in range(k):
            sol = random.choice(self.population)
            if best is None or cost(sol, self.dict) < cost(best, self.dict):
                best = sol
        return best

    def select_parents(self):
        parents = []
        for i in range(self.pop_size):
            parents.append(self.tournament_selection(3))
        return parents

    def crossover(self, parents):
        children = []
        for i in range(self.pop_size):
            if np.random.rand() < self.crossover_rate:
                parent1 = parents[i]
                parent2 = parents[np.random.randint(self.pop_size)]
                child = copy.deepcopy(parent1)
                #############################
                children.append(child)
            else:
                children.append(parents[i])

        return children

    def mutate(self, children):
        for i in range(self.pop_size):
            if np.random.rand() < self.mutation_rate:
                continue
        return children

    def elitism(self, children):
        children.sort(key=lambda x: cost(x, self.dict))
        for i in range(int(self.elitism_rate*self.pop_size)):
            children[i] = self.population[i]
        return children

    def verify(self, children):
        #remove invalid solutions
        for i in range(self.pop_size):
            if not self.valid(children[i], self.dict):
                children[i] = self.random_sol()
        return children
        
    def count_valid(self, children):
        count = 0
        for i in range(self.pop_size):
            if self.valid(children[i], self.dict):
                count += 1
        return count

    def run(self):
        self.init_population()
        for i in range(self.max_gen):
            self.compute_fitness()
            parents = self.select_parents()
            children = self.crossover(parents)
            children = self.mutate(children)
            children = self.elitism(children)
            children = self.verify(children)
            self.population = children
            if cost(self.population[0], self.dict) < self.best_cost:
                self.best_cost = cost(self.population[0], self.dict)
                self.best_sol = self.population[0]
                if self.best_cost < 1000000:
                    print("Generation: ", i, " Cost: ", self.best_cost, " Valid: ", self.valid(self.best_sol, self.dict))
            if i % 100 == 0:
                print("Generation", i+1, "Best cost:", self.best_cost)
                print("Valid solutions:", self.count_valid(self.population))
            wandb.log({"Generation": i, "Best cost": self.best_cost, "Valid solutions": self.count_valid(self.population)})