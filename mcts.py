import random
import sys
import copy 
import numpy as np
from functions import *
import wandb

class MonteCarloTreeSearch:
    def __init__(self, dict, solution, max_depth, c, default_cost, n_children):
        self.dict = dict
        self.solution = solution
        self.max_depth = max_depth
        self.best_cost = default_cost
        self.best_sol = None
        self.c = c
        self.best_costs = []
        self.root = {'solution':solution, 'n':0, 'cost':0, 'children':[], 'parent':None}
        self.n_children = n_children
        self.constraint = Constraint(self.dict)
        self.valid = self.constraint.valid

    def selection(self,node):
        x_i = 0
        s_i = 0
        if node['n'] != 0:
            x_i = (1/(node['cost']+1e-8))/node['n']
            s_i = np.sqrt(2*np.log(node['parent']['n'])/node['n'])
        return x_i + self.c*s_i

    def expansion(self, node, depth):
        for possibility in []:
            child = copy.deepcopy(node)
            child['solution'] = copy.deepcopy(node['solution'])
            child['parent'] = node
            child['n'] = 0
            child['cost'] = 0
            child['children'] = []
            if self.valid(child['solution'], self.dict):
                node['children'].append(child)
        return node
    
    def simulation(self,node):
        new_sol = copy.deepcopy(node['solution'])
        new_sol = self.__mutate__(new_sol)
        cost = cost(new_sol, self.dict)
        return cost

    def backpropagation(self,node, cost):
        node['n'] += 1
        node['cost'] += cost
        if node['parent'] != None:
            self.backpropagation(node['parent'], cost)

    def run(self):
        for i in range(self.max_depth):
            node = self.root
            while len(node['children']) != 0:
                node = max(node['children'], key=self.selection)
            node = self.expansion(node, i)
            for child in node['children']:
                cost = self.simulation(child)
                self.backpropagation(child, cost)
            if cost(node["solution"],self.dict) < self.best_cost:
                self.best_cost = cost(node["solution"],self.dict)
                self.best_sol = node['solution']
            print('Iteration: ', i, 'Best cost: ', self.best_cost)
            wandb.log({"Iteration": i, "Best cost": self.best_cost})
            self.best_costs.append(self.best_cost)
            self.root = node
        node = self.root
        while len(node['children']) != 0:
            node = max(node['children'], key=self.selection)
        if cost(node["solution"],self.dict) < self.best_cost:
            self.best_cost = cost(node["solution"],self.dict)
            self.best_sol = node['solution']
        print('Best cost: ', self.best_cost)
        return self.best_sol

    def __mutate__(self, solution):
        for all_possibilities_descendig_tree in []:
            continue
        return solution