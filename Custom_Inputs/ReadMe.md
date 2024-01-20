# Custom Inputs for a Metabolic Network

Please use the file [*Custom_Bacteria.py*](../Custom_Inputs/Custom_Bacteria.py) to modify the bacteria.

## Data:
- LB  The reactions' lower bounds [*LB.txt*](../Custom_Inputs/LB.txt)
- UB  The reactions' upper bounds [*UB.txt*](../Custom_Inputs/UB.txt)
- SSM The reactions Stoichiometric matrix [*SSM.txt*](../Custom_Inputs/SSM.txt)
- Rxn The reactions names' or ids [*Rxn.txt*](../Custom_Inputs/Rxn.txt)
- Met The metabolites names or ids [*Met.txt*](../Custom_Inputs/Met.txt)

LB,UB and Rxn are vectors of size M
Met is a vector of size N
SSM is a matrix of size NxM

### For a seamless work and no need for a major code modification keep the naming convention

#### Inside <Custom_Bacteria.py>
 The biological Assumptions can be modified in this file.

 Requirements:
  - biomass -> referes to the index associated with the cellular growth
  - chemical -> refers to the desired chemical to optimize
 
 when setting the bacteria object

  ```
  CB = Bacteria(S=S,LB=lb,UB=ub,Rxn=Rxn,Met=Met,Name='Custom',biomass=biomass,chemical=chemical)

  ```
   - `S=S` sets the Stoichiometic matrix
   - `LB=lb` sets  the lower bounds
   - `Ub=ub` sets the upper bounds
   - `Rxn=Rxn` sets the naming convention for the reactions
   - `Met=Met` sets the naming convention of the metabolites
   - `Name=` this can be changed to any name that identifies the bacteria
   - `biomass=` sets the cellular growth index
   - `chemical=` sets the desired chemical index
   - `KO=KO` sets the vector with potential reactions (indices),by default is set to `None`
   - `infeas=` sets the infeasibility for the solver, by default is set to `1e-6`
   - `time_limit=` sets a time limit for the solver, by default is set to `1000` seconds
   - `BM=` sets the Big M used in the solver to add constraints, by default is set to `1000`
