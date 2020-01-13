import runExtScript
import pathFolder
import DBrequest

from os import listdir, path
from copy import deepcopy

class MapAssaysToBody:
    def __init__(self, cToxCast, cNextBio, porgan, plot, prout):
        self.prout = prout
        self.ToxCast = cToxCast
        self.NextBio = cNextBio
        self.plot = plot
        self.porgan = porgan


    def loadOrgan(self):
        filin = open(self.porgan, "r")
        llines = filin.readlines()
        filin.close()

        dout = {}
        for line in llines[1:]:
            lelement = line.strip().replace("\"", "")
            lelement = lelement.split(",")
            system = lelement[0]
            subsystem = lelement[1]
            maporgan = lelement[2]
            if not system in list(dout.keys()):
                dout[system] = {}
            dout[system][subsystem] = maporgan
        self.dorgan = dout


    def premapAssays(self, dmapinfo):

        if not "dorgan" in self.__dict__:
            self.loadOrgan()

        lout = []
        for assay in self.ToxCast.dassays.keys():
            dassays = {}
            dassays["name"] = assay
            maptype = dmapinfo[assay]["Type of body mapping"]
            dassays["Type map"] = maptype
            if maptype == "viability":
                dassays["gene"] = "NA"
                dassays["system"] = "Immune System"
                dassays["organ"] = "Immune System"
                lout.append(deepcopy(dassays))

                dassays["system"] = "Digestive System"
                dassays["organ"] = "Liver"
                lout.append(deepcopy(dassays))

                dassays["system"] = "Respiratory System"
                dassays["organ"] = "Lung"
                lout.append(deepcopy(dassays))

                dassays["system"] = "Digestive System"
                dassays["organ"] = "Stomach"
                lout.append(deepcopy(dassays))
            
            elif maptype == "tissue":
                dassays["gene"] = "NA"
                organ = dmapinfo[assay]["Tissue"]
                if organ == "vascular":
                        dassays["system"] = "Cardiovascular System"
                        dassays["organ"] = "Vascular"
                else:
                    for system in self.dorgan.keys():
                        if organ.capitalize() in list(self.dorgan[system].keys()):
                            dassays["system"] = system
                            dassays["organ"] = organ.capitalize()
                            break
                
                lout.append(dassays)
            
            else:
                lgene = self.ToxCast.dassays[assay].charac["intended_target_gene_symbol"].upper().replace("\"", "").replace("/", "|").split("|") # case where one assays is mapped on several gene
                for gene in lgene:
                    dassays["gene"] = gene
                    dassays["system"] = "NA"
                    dassays["organ"] = "NA"
                    lout.append(dassays)
            

        pfilout = self.prout + "preMapping.csv"
        filout = open(pfilout, "w")
        filout.write("Assays\tgene\ttype mapping\tsystem\torgan\n")
        for assay in lout:
            filout.write("%s\t%s\t%s\t%s\t%s\n" %(assay["name"], assay["gene"], assay["Type map"], assay["system"], assay["organ"]))
        filout.close()

        self.lassays = lout


    def getGeneExpression(self, inDB = 0):
        if not "lassays" in self.__dict__:
            print("LOAD ASSAYS FIRST !")
            self.err = 1
            return 

        cDB = DBrequest.DBrequest()

        
        prgene = pathFolder.createFolder(self.prout + "geneExp/")
        for assay in self.lassays:
            if assay["gene"] != "NA":
                pgene = prgene + assay["gene"] + ".csv"
                if path.exists(pgene):
                    pass
                
                filgene = open(pgene, "w")
                filgene.write("system\torgan\texp\tcontrol\n")

                dgene = self.NextBio.runGeneToBodyAtlas(assay["gene"])
                dw = {}
                for system in dgene.keys():
                    dw[system] = {}
                    for organ in dgene[system].keys():
                        organw = self.dorgan[system][organ]
                        if not organw in list(dw[system].keys()):
                            dw[system][organw] = {}
                            dw[system][organw]["exp"] = []
                            dw[system][organw]["control"] = []
                        dw[system][organw]["control"].append(float(dgene[system][organ]["control"]))
                        dw[system][organw]["exp"].append(float(dgene[system][organ]["expression"]))
                    
                for system in dw.keys():
                    for organw in dw[system].keys():
                        filgene.write("%s\t%s\t%s\t%s\n"%(system, organw, max(dw[system][organw]["exp"]), max(dw[system][organw]["control"])))

                        # add in DB
                        if inDB == 1:
                            cDB.addElement("bodymap_genemap", ["gene", "control", "expression", "system", "organ"], [assay["gene"], max(dw[system][organw]["control"]), max(dw[system][organw]["exp"]), system, organw])

                filgene.close()




    def refineMappingWithExp(self, nbfold, prout, w=1):

        pranalysis = pathFolder.createFolder(prout + "analysisGene-" + str(nbfold) + "/")

        #if len(listdir(pranalysis)) > 10:
        #    return

        dtissus = {}
        for gene in self.dgene.keys():
            for organ in self.dgene[gene]["expression"].keys():
                for tissus in self.dgene[gene]["expression"][organ].keys():
                    kout = organ + "-" + tissus
                    if not kout in list(dtissus.keys()):
                        dtissus[kout] = {}
                        dtissus[kout]["gene"] = {}
                        dtissus[kout]["assays"] = {}

                    exp = float(self.dgene[gene]["expression"][organ][tissus]["expression"])
                    control = float(self.dgene[gene]["expression"][organ][tissus]["control"])
                    if exp > nbfold*control:
                        dtissus[kout]["gene"][gene] = {}
                        dtissus[kout]["gene"][gene]["exp"] = [exp, control]
                        dtissus[kout]["gene"][gene]["assays"] = self.dgene[gene]["Assays"]

                        for assays in self.dgene[gene]["Assays"]:
                            if not assays in list(dtissus[kout]["assays"].keys()):
                                dtissus[kout]["assays"][assays] = []

                            # fix here
                            if not gene in dtissus[kout]["assays"][assays]:
                                dtissus[kout]["assays"][assays].append(gene)


        if w == 1:
            fcount = open(pranalysis + "count.csv", "w")
            fcount.write("Organ-tissus\tNgene\tNassay\n")

            dcount = {}
            for k in dtissus.keys():
                dcount[k] = {}
                dcount[k]["gene"] = len(list(dtissus[k]["gene"].keys()))
                dcount[k]["assays"] = len(list(dtissus[k]["assays"].keys()))

                fcount.write("%s\t%s\t%s\n"%(k, dcount[k]["gene"], dcount[k]["assays"]))

                pfiloutGene = pranalysis + k + "_gene.csv"
                pfiloutAssays = pranalysis + k + "_assays.csv"
                filoutGene = open(pfiloutGene, "w")
                filoutGene.write("Gene\tExp\tcontrol\tAssays\n")
                filoutAssays = open(pfiloutAssays, "w")
                filoutAssays.write("Assay\tGenes\tExp\n")

                for gene in dtissus[k]["gene"].keys():
                    filoutGene.write("%s\t%s\t%s\t%s\n"%(gene, dtissus[k]["gene"][gene]["exp"][0], dtissus[k]["gene"][gene]["exp"][1], " ".join(dtissus[k]["gene"][gene]["assays"])))

                for assays in dtissus[k]["assays"].keys():
                    lgeneAssays = dtissus[k]["assays"][assays]# only take the first gene !!!!!!!!!
                    geneAssays = lgeneAssays[0]
                    filoutAssays.write("%s\t%s\t%s\n"%(assays, geneAssays, round(dtissus[k]["gene"][geneAssays]["exp"][0]/dtissus[k]["gene"][geneAssays]["exp"][1],3)))
                filoutAssays.close()

                filoutGene.close()

            fcount.close()

            runExtScript.histCountGeneAssays(pranalysis + "count.csv")
        return dtissus




