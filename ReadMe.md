# Metabolic Engineering Knockouts - Bilevel Linear Programming

You can use this package to solve the bilevel problem of reaction knockouts in metabolic engineering. I implemented an algorithm that exploits the bounds of the variables and adds feasibility cuts and no good cuts to find the best reaction knockout. The package includes data on E. Coli Bacteria, iJO1366, iAF1260, iJR904 and a Yeast Strain that were used to test the algorithm. But, the package also accepts custom bacteria.

## Inputs 
Parameteres for the algorithm use the *params.json* file. 
- **pct_grow** -> to set the growth percentage (minimal bacteria growth) to the wildtype "int" between 0-100. 
- **K** -> the number of allowed Knockouts "int". 
- **Apr** -> to distinguish between the optimistic and pessimistic aproach of the solution. 
- **Bacteria** -> to set the bacteria to use for the solution by wrting a text string with the names of the baceria. Otherwise, type in "Custome" for a custome bacteria and set the data in the "Custom_Inputs" [here](../main/Custom_Inputs) folder and custom chemical production. 
- **FileName** -> The name of the file where the results will be saved. The file is saved in the same folder where params.json and main.py are located. 

## Outputs
 - The name of the Bacteria.
 - The solving time from the solver in seconds.
 - The Strategy, that is the reaction Knockouts.
 - The chemical production for the specified chemical (objective function).
 - The biomass (cellular growth) for the mutant bacteria.
 - The binary vector that corresponds with the allowed reactions in the metabolic network (y=1) and the reaction knockouts (y=0).
 - The mass flow, that is the vector with the reactions' mass flow. 

 ### For a seamless work and no need for a major code modification keep the naming convention