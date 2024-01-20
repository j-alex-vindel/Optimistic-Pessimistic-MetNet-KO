import json
from collections import namedtuple
from typing import List,NewType
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import copy

PARAMS = namedtuple('Params',["K","pctgrow","Bacteria","Approach","Outfile"])
S_M = List[List[int]]
L_B = List[int]
U_B = List[int]
RXN = List[str]
MET = List[str]
KOS = List[int]
B_M = NewType('Big M',int)
TGT = NewType('Target',float)
IDX = NewType('Index',int)
WT = NewType('Wildtype',bool)
MT = NewType('Mutant',bool)
FBA = NewType('Flux Vector',List[float])
L = List[int]

class Example:
    def __init__(self,name):
        print(f"Example -> {name}")


class Parameters:
    def __init__(self,filename):
        self.filename = filename
   

    def assign_params(self):
        with open(self.filename,"r") as file:
            data = json.load(file)
            self.K = data['K']
            self.pctgrow = float(data['pct_grow']/100)
            self.Bacteria = data['Bacteria'].lower()
            self.aproach = data['Apr'].lower()
            self.outfile = data["FileName"]
        return PARAMS(self.K,self.pctgrow,self.Bacteria,self.aproach,self.outfile)
   
# P = Parameters("params.json").assign_params()

# print(P)

class Bacteria:
    def __init__(self,
                 S:S_M=None,
                 LB:L_B=None,
                 UB:U_B=None,
                 Rxn:RXN=None,
                 Met:MET=None,
                 KO:KOS=None,
                 Name:str=None,
                 biomass:IDX=None,
                 chemical:IDX=None,
                 infeas:float=1e-6,
                 time_limit:int=1000,
                 BM:B_M=1000,
                 ):
        self.S = S
        self.LB = LB
        self.UB = UB
        self.S = S
        self.LB = LB
        self.UB = UB
        self.Rxn = Rxn
        self.Met = Met
        self.KO = KO
        self.Name = Name
        self.biomass = biomass
        self.chemical = chemical
        self.infeas = infeas
        self.time_limit = time_limit
        self.BM = BM
        self.M = set_constructor(self.Rxn)
        self.N = set_constructor(self.Met)
        self.b = np.array([0 for i in self.N])
        self.c = np.array([1 if i == self.biomass else 0 for i in self.M])
        self.tgt = .5
        self.FBA = WT_FBA(self)
        self.FVA = WT_FBA(self,wt=False,mt=True)

    @property
    def tgt(self):
        return self._tgt
    @tgt.setter
    def tgt(self,tgt:TGT=.5):
        self._minprod = None
        self._tgt = tgt
    @property
    def minprod(self):
        if self._minprod is None:
            self._minprod = self._tgt*self.FBA[self.biomass]
        return self._minprod
    

def WT_FBA(mn,wt:WT=True,mt:MT=False) -> FBA:
    LB_wt = copy.deepcopy(mn.LB)
    UB_wt = copy.deepcopy(mn.UB)

    if wt and not mt:
        obj = mn.biomass
        FVA = False
    elif mt and not wt:
        obj = mn.chemical
        FVA=True
    else:
        raise Exception('Both wildtype and mutant cannot be TRUE or FALSE at the same time')
    
    fba = gp.Model()
    fba_v = fba.addVars(mn.M,lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='vs')
    vs = [fba_v[i] for i in mn.M]

    fba.setObjective(1*fba_v[obj],GRB.MAXIMIZE)
    fba.addMConstr(mn.S,vs,'=',mn.b,name='Stoi')
    fba.addConstrs((LB_wt[j] <= fba_v[j] for j in mn.M), name='LBwt')
    fba.addConstrs((UB_wt[j] >= fba_v[j] for j in mn.M), name='UBwt')
    if FVA:
        fba.addConstr((fba_v[mn.biomass] >= mn.minprod), name='minprod')

    fba.Params.OptimalityTol = mn.infeas
    fba.Params.IntFeasTol = mn.infeas
    fba.Params.FeasibilityTol = mn.infeas
    fba.Params.OutputFlag = 0
    fba.optimize()

    if fba.status == GRB.OPTIMAL:
        fbavs =  [fba.getVarByName('vs[%s]'%a).x for a in mn.M] 
    else:
        fbavs = [-2000 for _ in mn.M]

    return fbavs

def set_constructor(L) -> L:
    if L != None:
        return [_ for _ in range(len(L))]