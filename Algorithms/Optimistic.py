import sys
sys.path.append("..")

import gurobipy as gp
from gurobipy import GRB 
from itertools import combinations
import math
import copy
from typing import NewType,Type,List
from collections import namedtuple
from Support.S_Objects import Bacteria

M_Network = Type[Bacteria] 
Ks = NewType('Knockouts',int)
Vector = List[int]
Result = namedtuple('Result_cb',['MetNet','Strategy','Ys','Vs','Vij','Time','Soltype','Method'])

def O_Test(message):
    print(f"Optimistic Test -> {message}")

def A_Optimistic(network:M_Network=None,k:Ks=None,log:bool=True,speed:bool=False,threads:bool=False,extra:bool=False) -> Result:
    '''
    --------- Input -------------------------
    network      = Metabolic Network, default value None
    k            = Number of reactions to knockout, set to None
    log          = Option to show the log from the computation, set to True
    speed        = Option to try to decrease the computation time set to False
    threads      = Option to try to increase the number of available threads 

    --------- OutPut ------------------------
    cb = CB_solve_2_NOP(network=network,k=k,log=True,speed=False,threads=False)
        
    cb.MetNet    = Metabolic Network's name
    cb.Stragtegy = List of rxn to knockout
    cb.Ys        = Binary solution as a vector
    cb.Vs        = Optimal bilevel flows
    cb.Vij       = Flows in the inner problem
    cb.Time      = Solving time 
    cb.Soltype   = Type of solution [optimal, timelimit , infeasible]
    cb.Method    = Solving Method - set to CBO (Callbacks-Optimistic)

    '''
    
    lb = copy.deepcopy(network.LB)
    ub = copy.deepcopy(network.UB)
    minprod = copy.deepcopy(network.minprod)
    lb[network.biomass] = minprod

    def inner(imodel, yoj:Vector):

        imodel.setAttr('LB',imodel.getVars(),[lb[j]*yoj[j] for j in network.M])
        imodel.setAttr('UB',imodel.getVars(),[ub[j]*yoj[j] for j in network.M])
        imodel.Params.OptimalityTol = network.infeas
        imodel.Params.IntFeasTol = network.infeas
        imodel.Params.FeasibilityTol = network.infeas
        imodel.Params.Presolve = 0
        imodel.optimize()
        status = imodel.status
        if status == GRB.OPTIMAL:
            vij = [imodel.getVarByName('fv[%s]'%a).x for a in network.M] 
        elif status in (GRB.INFEASIBLE, GRB.UNBOUNDED, GRB.INF_OR_UNBD):
            vij = [2000 if i == network.biomass else yoj[i] for i in network.M]
        return vij,status

    def lazycall(model,where):
        if where == GRB.Callback.MIPSOL:
            model._voj = model.cbGetSolution(model._vars)
            model._yoj = model.cbGetSolution(model._varsy)
            knockset =  [i for i,y in enumerate(model._yoj) if model._yoj[i] < 1e-6]

            if len(knockset) != k:
                return
            cur_obj = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
            cur_bd = model.cbGet(GRB.Callback.MIPSOL_OBJBND)

            model._vi, inner_status = inner(model._inner, model._yoj)

# ============================ Checking Inner Optimality Status ===================================
            if inner_status != GRB.OPTIMAL:

                model.cbLazy(sum(model._varsy[j] for j in knockset) >=1)
                return
            
            else:
                vi_biom_val = model._vi[network.biomass]
                vi_chem_val = model._vi[network.chemical]
                knockset_inner = (i for i,y in enumerate(model._vi) if abs(model._vi[i]) < 1e-6 and i in network.KO)
                ki = (i for i in combinations(knockset_inner,k))
                
                if model._pbnd - model._vi[network.chemical] >= -1e-6: 

                    model.cbLazy(sum(model._varsy[j] for j in knockset) >= 1)

                    return
                elif (abs(model._vi[network.biomass] - model._voj[network.biomass]) > 1e-6):
                    model.cbLazy(vi_biom_val <= model._vars[network.biomass] + (math.ceil(model._vi[network.biomass]*10)/10) *(sum(model._varsy[f] for f in knockset)))
                    if extra:
                        for comb in ki:
                            
                            model.cbLazy(vi_biom_val <= model._vars[network.biomass] +
                                (math.ceil(model._vi[network.biomass]*10)/10) *(sum(model._varsy[f] for f in comb)))
                           
                    return
                else:

                    model._pbnd = cur_obj
                    return
# =============================================================================================================================                        

    m = gp.Model()

    m.Params.OptimalityTol = network.infeas
    m.Params.IntFeasTol = network.infeas
    m.Params.FeasibilityTol = network.infeas
    m.Params.Presolve = 0
    m.Params.PreCrush = 1

    cbv = m.addVars(network.M,lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='cbv')
    cby = m.addVars(network.M,vtype=GRB.BINARY,name='cby')
    cbvs = [cbv[i] for i in network.M]

    m.setObjective(1*cbv[network.chemical],GRB.MAXIMIZE)
    
    m.addMConstr(network.S,cbvs,'=',network.b,name='Stoi')
  

    m.addConstr(cbv[network.biomass] >= minprod, name='target')

    m.addConstrs((lb[j]*cby[j] <= cbv[j] for j in network.M),name='LB')
    m.addConstrs((cbv[j] <= ub[j]*cby[j] for j in network.M),name='UB')
    
    if network.KO is not None:
        m.addConstr(sum(1-cby[j] for j in network.KO) == k, name='knapsack')
        m.addConstrs((cby[j]==1 for j in network.M if j not in network.KO),name='Essen')
        
    elif network.KO is None:
        m.addConstr(sum(1-cby[j] for j in network.M) == k, name='knapsack')


    imodel = gp.Model()
    fv = imodel.addVars(network.M,lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='fv')
    fvs = [fv[i] for i in network.M]
    imodel.params.LogToConsole = 0
    imodel.setObjective(2000*fv[network.biomass] + fv[network.chemical], GRB.MAXIMIZE)
    
    imodel.addMConstr(network.S,fvs,'=',network.b,name='Stoi')
    
    
    imodel.addConstr(fv[network.biomass] >= minprod, name='target2')

    imodel.update()
    
    m._inner = imodel.copy()

    m._vars = cbv
    m._varsy = cby
    m.Params.lazyConstraints = 1
    m._pbnd = -1000
    m._cbcnt = 0
    m._sv = [0 for i in network.M]
    m._sy = []
    lazycts = []
    m._vi = None 
  
    if not log: m.Params.OutputFlag = 0
    if speed: m.Params.NodefileStart = 0.5
    if threads: m.Params.Threads = 6
  
    m.Params.TimeLimit = network.time_limit
   
    m.optimize(lazycall)
    
    cb_time = round(m.Runtime,4)
    vij = m._vi

    if m.status == GRB.OPTIMAL:
        ys = [m.getVarByName('cby[%d]'%j).x for j in network.M]
        vss = [m.getVarByName('cbv[%d]'%j).x for j in network.M]
        del_strat_cb = [network.Rxn[i] for i in network.M if ys[i] < .5]
        soltype = 'Optimal'
    elif m.status == GRB.TIME_LIMIT:
        ys = [m.getVarByName('cby[%d]'%j).x for j in network.M]
        vss = [m.getVarByName('cbv[%d]'%j).x for j in network.M]
        del_strat_cb = [network.Rxn[i] for i in network.M if ys[i] < .5]
        soltype = 'Time_Limit'

    elif m.status in (GRB.INFEASIBLE,GRB.UNBOUNDED, GRB.INF_OR_UNBD):
        ys = ['all' for i in network.M]
        vss = ['~' for i in network.M]
        del_strat_cb = ['all']
        soltype = 'Infeasible'
    

    return Result(network.Name,del_strat_cb,ys,vss,vij,cb_time,soltype,'CBO')
