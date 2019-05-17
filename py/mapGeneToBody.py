import runExtScript
import pathFolder


class MapGeneToBody:
    def __init__(self, cToxCast, cNextBio, prout):
        self.prout = prout
        self.ToxCast = cToxCast
        self.NextBio = cNextBio


    def map(self):

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
                runExtScript.histExpresion(pfilout)

        self.dgene = dgene


