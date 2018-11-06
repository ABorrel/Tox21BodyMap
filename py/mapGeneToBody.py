import ToxCast
import nextbio



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
                dgene[gene]["Tissu"] = []
            dgene[gene]["Assays"].append(assay)
            self.NextBio.runGeneToBodyAtlas(gene)
            print gene
            ddd
