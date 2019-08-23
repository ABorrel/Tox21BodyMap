



class mapChem:

    def __init__(self, cTC, cGenBody, prout):
        self.cTC = cTC
        self.cGeneBody = cGenBody
        self.prout = prout

    def map(self):

        pfilout = self.prout + "chemical.csv"
        filout = open(self.prout + "chemical.csv", "w")


        dout = {}
        ltissus = []
        for CASID in self.cTC.dchem.keys():
            dout[CASID] = {}
            if "activeAssays" in self.cTC.dchem[CASID].__dict__:
                for activeAssays in self.cTC.dchem[CASID].activeAssays.keys():
                    for gene in self.cGeneBody.dgene.keys():
                        for assays in self.cGeneBody.dgene[gene]["Assays"]:
                            if assays == activeAssays:
                                for system in self.cGeneBody.dgene[gene]["expression"].keys():
                                    for tissus in self.cGeneBody.dgene[gene]["expression"][system].keys():
                                        if not tissus in ltissus:
                                            ltissus.append(tissus)
                                        if not tissus in list(dout[CASID].keys()):
                                            dout[CASID][tissus] = {}
                                            dout[CASID][tissus]["lAC50"] = []
                                            dout[CASID][tissus]["expression"] = []
                                            dout[CASID][tissus]["control"] = []
                                            dout[CASID][tissus]["SD"] = []
                                        dout[CASID][tissus]["lAC50"].append(self.cTC.dchem[CASID].activeAssays[activeAssays])
                                        dout[CASID][tissus]["expression"].append(self.cGeneBody.dgene[gene]["expression"][system][tissus]["expression"])
                                        dout[CASID][tissus]["control"].append(self.cGeneBody.dgene[gene]["expression"][system][tissus]["control"])
                                        if self.cGeneBody.dgene[gene]["expression"][system][tissus]["SD"] != None:
                                            dout[CASID][tissus]["SD"].append(self.cGeneBody.dgene[gene]["expression"][system][tissus]["SD"])
                                        else:
                                            dout[CASID][tissus]["SD"].append("NA")





        filout.write("CASID\t%s\n"%("\t".join([t + "_AC50\t" + t + "_expression\t" + t + "_control\t" + t + "_SD" for t in ltissus])))
        for CASID in dout.keys():
            filout.write(CASID)
            for tissus in ltissus:
                if tissus in list(dout[CASID].keys()):
                    print (dout[CASID][tissus])

                    filout.write("\t%s\t%s\t%s\t%s"%(" ".join(dout[CASID][tissus]["lAC50"]),
                                                         " ".join(dout[CASID][tissus]["expression"]),
                                                         " ".join(dout[CASID][tissus]["control"]),
                                                         " ".join(dout[CASID][tissus]["SD"])))
                else:
                    filout.write("\tNA\tNA\tNA\tNA")

            filout.write("\n")
        filout.close()
