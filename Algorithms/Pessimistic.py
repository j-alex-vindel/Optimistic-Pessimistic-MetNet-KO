import gurobipy as gp
from gurobipy import GRB 
from itertools import combinations
import math

def A_Pessimistic(message):
    print(f'Pessimistic -> {message}')