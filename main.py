import Support

# ---- Reading and setting Parameters ----

P = Support.Parameters("params.json").assign_params()

# ---- Reading and setting the metabolic network ----
mn = Support.bacteriaselector(P.Bacteria)

mn.tgt = P.pctgrow
# ---- Setting the optimization approach ----
solve = Support.Select_Approach(P.Approach)

# ---- Solving the bilelvel probem ----
r = solve(network=mn,k=P.K,log=False)

# ---- Saving the results ----
Support.SaveResults(result=r,filename=P.Outfile,metnet=mn)
