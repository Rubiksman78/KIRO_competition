import random
import sys
import copy 
from functions import *
import numpy as np
import wandb

class BranchAndBound:
    def __init__(self, dict, solution, max_depth, n_children,default_cost):
        self.dict = dict
        self.solution = solution
        self.max_depth = max_depth
        self.best_cost = sys.maxsize
        self.best_sol = None
        self.n_children = n_children
        self.default_cost = default_cost
        self.best_costs = []
        self.cost_at_depth = np.zeros(max_depth)
        self.constraint = Constraint(dict)
        self.valid = self.constraint.valid

    def run(self):
        self.__branch_and_bound__(self.solution, 0)
        return self.best_sol
        
    def __branch_and_bound__(self, solution, depth):
        if depth == self.max_depth:
            return
        cost = cost(solution, self.dict)
        if not self.__verify__(solution):
            return
        if (cost <= self.cost_at_depth[depth-1] or depth ==0) and (self.cost_at_depth[depth] == 0 or cost < self.cost_at_depth[depth]):
            self.cost_at_depth[depth] = cost
        else:
            return
        print("Depth: ", depth, " - Cost: ", cost, " - Best cost: ", self.best_cost)
        self.best_costs.append(self.best_cost)
        wandb.log({"Depth": depth, "Cost": cost, "Best cost": self.best_cost})
        if cost < self.best_cost:
            self.best_cost = cost
            self.best_sol = solution
    
        for child in range(self.n_children):
            child = self.__mutate__(solution)
            self.__branch_and_bound__(child, depth+1)
    

    def __verify__(self, solution):
        return self.valid(solution, self.dict)
        
    def __mutate__(self, solution):
        new_sol = copy.deepcopy(solution)
        #############################
        return new_sol