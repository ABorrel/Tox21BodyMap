import DBrequest
import pathFolder
from os import path
from re import search

def uploadAC50InDB(TC, nametable):

        cDB = DBrequest.DBrequest()
        lassays = list(TC.dassays.keys())

        for chem in TC.dchem.keys():
            for assay in lassays:
                if assay in list(TC.dchem[chem].activeAssays.keys()):
                    cDB.addElement(nametable, ["casn", "ac50", "assay"], [chem, TC.dchem[chem].activeAssays[assay], assay])
                    

def uploadGeneExpInDB(dAssayCleaned, cNB, dorgan, prout, w=0):
    """
    parms:
    - cAssayCleaned: class assays loaded from AssayMapping.py
    - cNB: class to load Nextbio data from nextbio.py
    - w: 1 if write expression by organ gene by gene and 0 no write
    - pr_out: path folder for w=1
    """

    # load cDB
    cDB = DBrequest.DBrequest()

    prgene = pathFolder.createFolder(prout + "geneExp/")
    for assay in list(dAssayCleaned.keys()):
        genes = dAssayCleaned[assay]["Gene"]
        print(genes)
        if genes != "NA" and genes != "" and dAssayCleaned[assay]["Type of body mapping"] == "gene target":
            if search("\|", genes):
                print(genes)
                genes = genes.split("|")
                print (gene)
            else:
                genes = [genes]
            
            for gene in genes:
                pgene = prgene + gene + ".csv"
                if path.exists(pgene):
                    pass
                if w == 1:
                    filgene = open(pgene, "w")
                    filgene.write("system\torgan\texp\tcontrol\n")

                dgene = cNB.loadGeneToBodyAtlas(gene)
                dw = {}
                for system in dgene.keys():
                    dw[system] = {}
                    for organ in dgene[system].keys():
                        organw = dorgan[system][organ]
                        if not organw in list(dw[system].keys()):
                            dw[system][organw] = {}
                            dw[system][organw]["exp"] = []
                            dw[system][organw]["control"] = []
                        dw[system][organw]["control"].append(float(dgene[system][organ]["control"]))
                        dw[system][organw]["exp"].append(float(dgene[system][organ]["expression"]))
                        
                for system in dw.keys():
                    for organw in dw[system].keys():
                        if w == 1:
                            filgene.write("%s\t%s\t%s\t%s\n"%(system, organw, max(dw[system][organw]["exp"]), max(dw[system][organw]["control"])))

                        # add in DB
                        cDB.addElement("bodymap_genemap", ["gene", "control", "expresson", "system", "organ"], [assay["gene"], max(dw[system][organw]["control"]), max(dw[system][organw]["exp"]), system, organw])
                if w ==1: 
                    filgene.close()