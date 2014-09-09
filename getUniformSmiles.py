#!/opt/az/psf/python/2.7/bin/python
from openeye.oechem import *

import cgi

#creates a list of smiles of the syntax [smiles|molId,smiles|molId]
def process_smiles(smiles):
    smiles = smiles.split('\n')
    mol = OEGraphMol()
    smiles_list=[]
    for line in smiles:
        if len(line.rstrip())>0:
            line = line.split()
            smi = line[0]
            molId = ""
            if len(line)>1:
                molId = line[1].replace(" ","|").rstrip()
            if(OEParseSmiles(mol,smi)):
                smi = OECreateSmiString(mol)
            mol.Clear()
            smiles_list.append(smi + "|" + molId) #can't send spaces or new lines

    return smiles_list

#takes a list of smiles and writes it as sdf using a memory buffer
def write_sdf(smiles_list):
    sdfs = []
    ofs = oemolostream()
    ofs.SetFormat(OEFormat_SDF)
    ofs.openstring()
    mol = OEGraphMol()
    for smiles in smiles_list:
        if(OEParseSmiles(mol,smiles.replace("|"," "))):
            OEWriteMolecule(ofs,mol)
            sdfs.append(ofs.GetString())
            mol.Clear()
            ofs.SetString("")
    return sdfs

#creates a list of smiles of the syntax [smiles|molId,smiles|molId]
def read_sdf(sdf_data):
    ifs = oemolistream()
    ifs.SetFormat(OEFormat_SDF)
    ifs.openstring(sdf_data)
    smiles_list = []
    for mol in ifs.GetOEGraphMols():
        smiles = OECreateSmiString(mol)
        smiles_list.append(smiles + "|" + mol.GetTitle())
    return smiles_list

if __name__ == "__main__":
    print "Content-Type: text/html\r\n\r\n"
    form = cgi.FieldStorage()

    extension = form.getvalue("extension")
    dataA  = form.getvalue("dataA") 
    operator = form.getvalue("smiles_operator") 
    sdf_output = form.getvalue("sdf_output")
    
    if(extension=="smi"):
        list_A = process_smiles(dataA)
    else:
        list_A = read_sdf(dataA)
 

    outputString = ""
    if(operator=="UNI"): #if only one file is supplied
        outputString = "*".join(set(list_A)) #removes all doubles using the set() function
    else:
        dataB  = form.getvalue("dataB") #if two files are supplied
        if(extension=="smi"):
            list_B = process_smiles(dataB)
        else:
            list_B = read_sdf(dataB)
        
        if(operator=="AND"):
            outputString = "*".join(set(list_A) & set(list_B))
        elif(operator=="OR"):
            outputString = "*".join(set(list_A) | set(list_B))
        elif(operator=="NOT"):
            outputString = "*".join(set(list_A) - set(list_B))


    if(sdf_output=="on"): #if we want the output as sdf
        sdfs = write_sdf(outputString.replace("|"," ").split("*"))
        outputString = "*".join(sdfs)
        outputString = outputString.replace("\n","!").replace(" ","|")

    #sends the output to index.html using javascript
    print """
    <html>
    <head>
    <input type="text" id="data" value=""" + outputString + """>
    <script type="text/javascript">
    parent.postMessage(data.value,"*");
    </script>

    </head>
    </html>
    """ 
