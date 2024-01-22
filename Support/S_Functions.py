import sys
import os

def bacteriaselector(bacteria:str=None):
    if bacteria != 'custom':

        sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Metabolic_Networks'))) 
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        mk = os.path.basename(path)

        dir = dir.replace(mk,"Metabolic_Networks")
        os.chdir(dir)
        match bacteria:
            case 'yeast':
                from YEAST import MN_Yeast
                met = MN_Yeast
            case 'ijo1366':
                from IJO import MN_ijo1366
                met = MN_ijo1366
            case 'iaf1260':
                from IAF import MN_iaf1260
                met = MN_iaf1260
            case 'ijr904':
                from IJR import MN_ijr904
                met = MN_ijr904
            case 'ijrmomo':
                from IJRMOMO import MN_MOMO_ijr
                met = MN_MOMO_ijr
            case 'ijrmomod':
                from IJRMOMOD import MN_MOMO_D
                met = MN_MOMO_D
            case _:
                raise Exception("No Metabolic Network's been selected")
    else:
        sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Custom_Inputs'))) 
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        mk = os.path.basename(path)

        dir = dir.replace(mk,"Metabolic_Networks")
        os.chdir(dir)
        from Custom_Bacteria import CB
        met = CB
    return met


def Select_Approach(approach:str=None):
    from Algorithms.Approaches import A_Optimistic,A_Pessimistic
    match approach:
        case 'optimistic':
            f = A_Optimistic
        case 'pessimistic':
            f = A_Pessimistic
        case _:
            raise Exception('Select an approach in the params json file')
    return f

def SaveResults(result:object=None,filename:str=None,metnet:object=None):
    space = '\n'
    os.chdir("../")
    
    with open(filename,"w+") as outfile:
        outfile.write("Bacteria: ")
        outfile.write(result.MetNet + space)
        
        outfile.write("Time (s): ")
        outfile.write(str(result.Time) + space)
        
        outfile.write('Strategy: ')
        outfile.writelines([ko +',' for ko in result.Strategy])
        outfile.write(space)
        
        outfile.write(f'Chemical ({metnet.Rxn[metnet.chemical]}):  ')
        outfile.writelines(str(round(result.Vs[metnet.chemical],4)))
        outfile.write(space)

        outfile.write(f'Biomass ({metnet.Rxn[metnet.biomass]}):  ')
        outfile.writelines(str(round(result.Vs[metnet.biomass],4)))
        outfile.write(space)

        outfile.write("Binary_Vector: ")
        outfile.writelines([str(i)+',' for i in result.Ys])
        outfile.write(space)

        outfile.write('Mass_Flow: ')
        outfile.writelines([str(i)+',' for i in result.Vs])
        outfile.write(space)

    print(f"File saved!")
