from functions import *
import random 
import math
import copy
import wandb

class SimulatedAnnealing:
    def __init__(self, dict, sol, max_iter, temp_init, temp_min, alpha):
        self.dict = dict
        self.sol = sol
        self.max_iter = max_iter
        self.temp_init = temp_init
        self.temp_min = temp_min
        self.alpha = alpha
        self.best_sol = sol
        self.best_cost = cost(sol, dict)
        self.current_sol = sol
        self.current_cost = cost(sol, dict)
        self.iter = 0
        self.temp = temp_init
        self.constraint = Constraint(dict)
        self.valid = self.constraint.valid

    def cosine_annealing(self):
        return self.temp_init / 2 * (1 + math.cos(self.iter * math.pi / self.max_iter))

    def run(self):
        while self.iter < self.max_iter and self.temp > self.temp_min:
            self.iter += 1
            self.temp = self.cosine_annealing()
            new_sol = self.generate_new_sol()
            new_cost = cost(new_sol, self.dict)
            if new_cost < self.current_cost:
                self.current_sol = new_sol
                self.current_cost = new_cost
                if new_cost < self.best_cost:
                    self.best_sol = new_sol
                    self.best_cost = new_cost
            else:
                if random.random() < math.exp(-(new_cost - self.current_cost) / self.temp):
                    self.current_sol = new_sol
                    self.current_cost = new_cost
            if self.iter % 1000 == 0:
                print("Iteration:", self.iter, "Cost:", self.current_cost, "Temp:", self.temp)
            wandb.log({"Iteration": self.iter, "Cost": self.current_cost, "Temp": self.temp})
        return self.best_sol

    def generate_new_sol(self):
        new_sol = copy.deepcopy(self.current_sol)
        return new_sol