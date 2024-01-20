# Custom Inputs for a Metabolic Network

Please use the file <custom_Baceria.py> to modify the bacteria.

## Data:
    - LB -> The reactions' lower bounds <LB.txt>
    - UB -> The reactions' upper bounds <UB.txt>
    - SSM -> The reactions Stoichiometric matrix <Met.txt>
    - Rxn -> The reactions names' or ids <Rxn.txt>
    - Met -> The metabolites names or ids <Met.txt>

LB,UB and Rxn are vectors of size M
Met is a vector of size N
SSM is a matrix of size NxM

### For a seamless work and no need for a major code modification keep the naming convention

#### Inside <Custom_Bacteria.py>
 The biological Assumptions can be modified in this file.

 Requirements:
  - biomass -> referes to the index associated with the cellular growth
  - chemical -> refers to the desired chemical to optimize
 
 