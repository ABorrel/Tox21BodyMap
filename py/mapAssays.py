from re import search

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
                dassays[assay]["Type"] = []
                dassays[assay]["tissue"] = self.cTC.dassays[assay].charac["tissue"]
                dassays[assay]["cell_short_name"] = self.cTC.dassays[assay].charac["cell_short_name"]
                dassays[assay]["assay_name"] = self.cTC.dassays[assay].charac["assay_name"]



        prresult = pathFolder.createFolder(self.prout + "mapAssays_" + str(nfolds) + "/")
        dGeneTissus = self.cGeneMapped.refineMappingWithExp(nfolds, prresult, w=0)


        for assay in dassays.keys():
            if dassays[assay]["source"] == "APR" or dassays[assay]["source"] == "LTEA" or dassays[assay]["source"] == "CLD":
                dassays[assay]["body"].append("Digestive System-Liver")
                dassays[assay]["Type"].append("Source")
            elif dassays[assay]["source"] == "BSK":
                dassays[assay]["body"].append("Immune System")
                dassays[assay]["Type"].append("Source")
            elif dassays[assay]["source"] == "CEETOX":
                dassays[assay]["body"].append("Nervous System")
                dassays[assay]["Type"].append("Source")

        for tissus in dGeneTissus.keys():
            for assay in dGeneTissus[tissus]["assays"].keys():
                if assay in list(dassays.keys()):
                    if not tissus in dassays[assay]["body"]:
                        dassays[assay]["body"].append(tissus)
                        dassays[assay]["Type"].append("Gene")


        for assay in dassays.keys():
            if dassays[assay]["tissue"] != "NA":
                tissue = dassays[assay]["tissue"].upper()
                flag = 0
                for bodypart in dassays[assay]["body"]:
                    print(bodypart)
                    if search(tissue, bodypart.upper()):
                        flag = 1
                        break
                if flag ==  0:
                    dassays[assay]["body"].append(dassays[assay]["tissue"])
                    dassays[assay]["Type"].append("Tissues")

        pfilout = prresult + "AssaysBody_" + str(nfolds) + ".csv"
        filout = open(pfilout, "w")
        filout.write("Assays\tSource\tGene\tTissues\tCell\tBody mapped\tType mapping\n")
        for assay in dassays.keys():
            if dassays[assay]["body"] != []:
                filout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(assay, dassays[assay]["source"], dassays[assay]["gene"],
                                                         dassays[assay]["tissue"], dassays[assay]["cell_short_name"],
                                                         "_".join(dassays[assay]["body"]),
                                                         "_".join(dassays[assay]["Type"])))
        filout.close()




        # develop by assays short name

        dassaysName = {}
        for assay in dassays.keys():
            name = dassays[assay]["assay_name"]
            if not name in list(dassaysName.keys()):
                dassaysName[name] = {}
                dassaysName[name]["gene"] = dassays[assay]["gene"]
                dassaysName[name]["source"] = dassays[assay]["source"]
                dassaysName[name]["cell_short_name"] = dassays[assay]["cell_short_name"]
                dassaysName[name]["tissue"] = dassays[assay]["tissue"]
                dassaysName[name]["body"] = dassays[assay]["body"]
                dassaysName[name]["Type"] = dassays[assay]["Type"]

        pfilout = prresult + "AssaysNameBody_" + str(nfolds) + ".csv"
        filout = open(pfilout, "w")
        filout.write("Assays\tSource\tGene\tTissues\tCell\tBody mapped\tType mapping\n")
        for assay in dassaysName.keys():
            if dassaysName[assay]["body"] != []:
                filout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(assay, dassaysName[assay]["source"], dassaysName[assay]["gene"],
                                                         dassaysName[assay]["tissue"], dassaysName[assay]["cell_short_name"],
                                                         "_".join(dassaysName[assay]["body"]),
                                                         "_".join(dassaysName[assay]["Type"])))
        filout.close()


