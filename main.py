import Support

# from Metabolic_Networks import IAF

P = Support.Parameters("params.json").assign_params()


mn = Support.bacteriaselector(P.Bacteria)

print(mn.Name)

mn.tgt = P.pctgrow

solve = Support.Select_Approach(P.Approach)

r = solve(network=mn,k=P.K)


Support.SaveResults(result=r,filename=P.Outfile)
