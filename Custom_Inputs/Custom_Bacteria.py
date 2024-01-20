import os
import sys
sys.path.append("..")

from Support.S_Objects import Bacteria,Example
from Read_Data import ReadData


Lb,Ub,S,Rxn,Met = ReadData()

# Declare index

biomass = 3 # Change this index to be the index of the growth or biomass
chemical = 5 # Change this index to the deisred Chemical

#------------ Biological Assumptions ---------------------
# Change here any biological assumptions and declare 

# Set a KO set if any


CB = Bacteria(S=S,LB=Lb,UB=Ub,Rxn=Rxn,Met=Met,Name='Custom',biomass=biomass,chemical=chemical)

