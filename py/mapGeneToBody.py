import runExtScript
import pathFolder

from os import listdir

class MapGeneToBody:
    def __init__(self, cToxCast, cNextBio, plot, prout):
        self.prout = prout
        self.ToxCast = cToxCast
        self.NextBio = cNextBio
        self.plot = plot


    def mapGene(self):

        dgene = {}
        for assay in self.ToxCast.dassays.keys():
            gene = self.ToxCast.dassays[assay].charac["intended_target_gene_symbol"].upper()
            if gene == "":  # case of assays without assays determinated
                continue
            if not gene in dgene.keys():
                dgene[gene] = {}
                dgene[gene]["Assays"] = []
                dgene[gene]["expression"] = {}
            dgene[gene]["Assays"].append(assay)
            dgene[gene]["expression"] = self.NextBio.runGeneToBodyAtlas(gene)
        lorgane = dgene[dgene.keys()[0]]["expression"].keys()

        for organ in lorgane:
            progan = pathFolder.createFolder(self.prout + organ.replace(" ", "_") + "/")
            ltissus = dgene[dgene.keys()[0]]["expression"][organ].keys()
            for tissu in ltissus:
                pfilout = progan + tissu.replace(" ", "_")
                filout = open(pfilout, "w")
                filout.write("gene\texpression\tSD\tcontrol\tAssays\n")

                for gene in dgene.keys():
                    if dgene[gene]["expression"] == {}: continue
                    filout.write("%s\t%s\t%s\t%s\t%s\n"%(gene, dgene[gene]["expression"][organ][tissu]["expression"],
                                                         dgene[gene]["expression"][organ][tissu]["SD"],
                                                         dgene[gene]["expression"][organ][tissu]["control"],
                                                         "--".join(dgene[gene]["Assays"])))

                filout.close()
                if self.plot == 1:
                    runExtScript.histExpresion(pfilout)
        self.dgene = dgene


    def refineMappingWithExp(self, nbfold, prout):

        pranalysis = pathFolder.createFolder(prout + "analysisGene-" + str(nbfold) + "/")

        #if len(listdir(pranalysis)) > 10:
        #    print "Already computed "
        #    return

        dtissus = {}
        for gene in self.dgene.keys():
            for organ in self.dgene[gene]["expression"].keys():
                for tissus in self.dgene[gene]["expression"][organ].keys():
                    kout = organ + "-" + tissus
                    if not kout in dtissus.keys():
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
                            if not assays in dtissus[kout]["assays"].keys():
                                dtissus[kout]["assays"][assays] = []

                            dtissus[kout]["assays"][assays].append(gene)

        fcount = open(pranalysis + "count.csv", "w")
        fcount.write("Organ-tissus\tNgene\tNassay\n")

        dcount = {}
        for k in dtissus.keys():
            dcount[k] = {}
            dcount[k]["gene"] = len(dtissus[k]["gene"].keys())
            dcount[k]["assays"] = len(dtissus[k]["assays"].keys())

            fcount.write("%s\t%s\t%s\n"%(k, dcount[k]["gene"], dcount[k]["assays"]))

            pfiloutGene = pranalysis + k + "_gene.csv"
            pfiloutAssays = pranalysis + k + "_assays.csv"
            filoutGene = open(pfiloutGene, "w")
            filoutGene.write("Gene\tExp\tcontrol\tAssays\n")
            filoutAssays = open(pfiloutAssays, "w")
            filoutAssays.write("Assay\tGenes\n")

            for gene in dtissus[k]["gene"].keys():
                filoutGene.write("%s\t%s\t%s\t%s\n"%(gene, dtissus[k]["gene"][gene]["exp"][0], dtissus[k]["gene"][gene]["exp"][1], " ".join(dtissus[k]["gene"][gene]["assays"])))

            for assays in dtissus[k]["assays"].keys():
                filoutAssays.write("%s\t%s\n"%(assays, " ".join(dtissus[k]["assays"][assays])))
            filoutAssays.close()

            filoutGene.close()

        fcount.close()

        runExtScript.histCountGeneAssays(pranalysis + "count.csv")
        return dtissus




