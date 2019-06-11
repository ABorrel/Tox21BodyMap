import pathFolder





class mapAssays:


    def __init__(self, cGeneMap, cTC, cNB, prout):
        self.cGeneMapped = cGeneMap
        self.cTC = cTC
        self.cNB = cNB
        self.prout = prout


    def map(self, nfolds, lassaysExcluded):

        dassays = {}
        for assay in self.cTC.dassays.keys():
            source = self.cTC.dassays[assay].charac["assay_source_name"]
            if source in lassaysExcluded:
                continue
            else:
                dassays[assay] = {}
                dassays[assay]["gene"] = self.cTC.dassays[assay].charac["intended_target_gene_symbol"].upper()
                dassays[assay]["source"] = source
                dassays[assay]["body"] = []


        prresult = pathFolder.createFolder(self.prout + "mapAssays_" + str(nfolds) + "/")
        dGeneTissus = self.cGeneMapped.refineMappingWithExp(nfolds, prresult)


        for tissus in dGeneTissus.keys():
            for assay in dGeneTissus[tissus]["assays"].keys():
                if assay in dassays.keys():
                    if dassays[assay]["source"] == "APR" or dassays[assay]["source"] == "LTEA":
                        if tissus == "Digestive System-Liver":
                            dassays[assay]["body"].append(tissus)
                    elif dassays[assay]["source"] == "BSK":
                        if tissus.split("-")[0] == "Immune System":
                            dassays[assay]["body"].append(tissus)
                    elif dassays[assay]["source"] == "CEETOX":
                        if tissus.split("-")[0] == "Nervous System":
                            dassays[assay]["body"].append(tissus)
                    else:
                        dassays[assay]["body"].append(tissus)


        pfilout = prresult + "AssaysBody.csv"
        filout = open(pfilout, "w")
        filout.write("Assays\tSource\tGene\tBody mapped\n")
        for assay in dassays.keys():
            filout.write("%s\t%s\t%s\t%s\n"%(assay, dassays[assay]["source"], dassays[assay]["gene"], "_".join(dassays[assay]["body"])))
        filout.close()




