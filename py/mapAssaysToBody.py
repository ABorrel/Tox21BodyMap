import runExtScript
import pathFolder
import DBrequest

from os import listdir, path
from copy import deepcopy

class mapAssaysToBody:
    def __init__(self, cNextBio, cAssays, porgan, prout):
        self.prout = prout
        self.NextBio = cNextBio
        self.porgan = porgan
        self.assays = cAssays


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




