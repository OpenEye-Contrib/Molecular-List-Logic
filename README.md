Molecular List Logic is web-app to perform logic operations on various molecular lists. 
by Magnus Norrby and Jonas Boström at AstraZeneca CVMD Sweden, 2014-08-31
###########################################################################

![Screenshot](https://github.com/OpenEye-Contrib/Molecular-List-Logic/blob/master/ScreenShotMolecularListLogic.GIF) 


**Componentents:**
css/bootstrap.css  //layout
images/and.png not.png or.png save.png  //these are images for logic operations and export
uploads/    // the folder where resultsfiles are written to be uploaded to the client
getUniformSmiles.py  // python-script to handle smiles and sdf files
write_file.php  // php-script that generate outputfile and write to LOGFILE.txt
LOGFILE.txt  // logfile
index.html  // interface and the javascript code
help.html  // some basic instructions
ScreenShotMolecularListLogic.GIF // a screenshot of interface

**index.html:**
Currently supported browsers are Firefox and Google Chrome. 
An error message will be shown in case any of the required functions (like draggable och filereader) are not supported.
In case draggable is missing, there's a standard file upload, instead of the drag and drop. 

**write_file.php:**
Writes the results from the form "resultat_form" in index.html to file in the uploads folder. 
Writes date and which boolean operation to LOGFILE.txt

**getUniformSmiles.py:**
Retrieves data from the form "get_uniform_smiles" and performs boolean operation
The data is then returned via the javascriptfunktion "parent.postMessage()"
This is done since the python script is a hidden iframe in index.html.
Please remember to change (#!/opt/az/psf/python/2.7/bin/python) to the correct python path  

**The app can hang if long/big txt lists are supplied (>30k), probably due to memory issues**

The function used for that is shown below (from file "getUniformSmiles.py")
def write_sdf(smiles_list):
    sdfs = []
    ofs = oemolostream()
    ofs.SetFormat(OEFormat_SDF)
    ofs.openstring()
    mol = OEGraphMol()
    for smiles in smiles_list:
        if(OEParseSmiles(mol,smiles)):
            OEWriteMolecule(ofs,mol)  # <----- here's where we write data to ofs memorybuffer
            sdfs.append(ofs.GetString()) # <---- here's where we get tan ostored in buffer
            mol.Clear()
            ofs.SetString("")
    return sdfs
