import itertools
import sys

#Define default solution for max cost and initialize algorithm
def default_solution():
    pass

#Define constraints
class Constraint:
    def __init__(self,dict):
        self.dict = dict

    def constraint_i(self,sol):
        pass

    def valid(self,sol):
        """
        Check if solution is valid
        Verify that all constraints are satisfied
        """
        pass

#Define cost function
def cost(sol,dict):
    pass

#Define initial solution
def default_solution():
    pass