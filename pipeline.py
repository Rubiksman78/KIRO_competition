import json
import random
import sys
import copy 
from algogen import AlgoGen
from bandb import BranchAndBound
from mcts import MonteCarloTreeSearch
from simul_anneal import SimulatedAnnealing
import wandb 
from functions import *

ALGO_NAME = "Simulated Annealing"
wandb.init(project="ponts", entity=ALGO_NAME)

#Load data dict
data = json.load(open(''))

#Print keys
print(data.keys())
print([example[0] for example in data['train']])

#Define algorithm
default_sol = default_solution()
default_cost = cost(default_sol, dict)
max_depth = len(default_sol) 
n_children =  len(default_sol)

c = 0.5
print("Default_cost:",cost(default_sol,dict))
print("Max depth:", max_depth)
print("c:", c)
print("Number of children:", n_children)

algo = SimulatedAnnealing(dict, default_sol, 100000, 100000, 1, 0.9999)

#Run algorithm
if __name__ == "__main__":
    best_sol = algo.run()
    print("Best solution: ", best_sol)
    print("Best cost: ", cost(best_sol, data))