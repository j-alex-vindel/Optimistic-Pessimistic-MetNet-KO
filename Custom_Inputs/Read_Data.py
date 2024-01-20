import os
import pandas as pd
def is_non_zero_path(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath)>0
def ReadData():
    try: 
        Lb = pd.read_csv(f"../Custom_Inputs/LB.txt",sep=" ",header=None)[0].tolist()
        Ub = pd.read_csv(f"../Custom_Inputs/UB.txt",sep=" ",header=None)[0].tolist()
        S = pd.read_csv(f"../Custom_inputs/SSM.txt",sep=" ",header=None).values
        Rxn = pd.read_csv(f"../Custom_Inputs/Rxn.txt",sep=" ",header=None)[0].tolist()
        Met = pd.read_csv(f"../Custom_Inputs/Met.txt",sep=" ",header=None)[0].tolist()
    except:
        raise Exception("Files must not be empty")
    return Lb,Ub,S,Rxn,Met  