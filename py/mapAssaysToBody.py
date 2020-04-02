import runExtScript
import pathFolder
import DBrequest

from os import listdir, path
from copy import deepcopy
from re import search
from numpy import median


class mapAssaysToBody:
    def __init__(self, cNextBio, dassays, dorgan, prout):
        self.prout = prout
        self.NextBio = cNextBio
        self.dorgan = dorgan
        self.dassays = dassays


    def analyseCountAssaysByExp(self, dgeneControl={}):
        pr_out = pathFolder.createFolder(self.prout + "AssaysByExp/")
        # define structure
        dout = {}
        for system in self.dorgan.keys():
            for org in self.dorgan[system].keys():
                organ = self.dorgan[system][org]
                if not organ in list(dout.keys()):
                    dout[organ] = {}
                    dout[organ]["No"] = 0.0
                    dout[organ][2] = 0.0
                    dout[organ][5] = 0.0
                    dout[organ][10] = 0.0
        
        for assay in self.dassays.keys():
            # calibrate a count unique
            dcount = {}
            if self.dassays[assay]["Type of body mapping"] == "viability":
                dout["Immune System"]["No"] = dout["Immune System"]["No"] + 1
                dout["Liver"]["No"] = dout["Liver"]["No"] + 1
                dout["Lung"]["No"] = dout["Lung"]["No"] + 1
                dout["Stomach"]["No"] = dout["Stomach"]["No"] + 1
                continue
            elif self.dassays[assay]["Type of body mapping"] == "tissue":
                tissue = self.dassays[assay]["Tissue"].capitalize()
                #print(tissue)
                for system in self.dorgan.keys():
                    if tissue in list(self.dorgan[system].keys()):
                        dout[self.dorgan[system][tissue]]["No"] = dout[self.dorgan[system][tissue]]["No"] + 1
                        break
                continue

            for organ in dout.keys():
                dcount[organ] = {2:0, 5:0, 10:0}
            
            if self.dassays[assay]["Type of body mapping"] == "gene target":
                genes = self.dassays[assay]["Gene"]
                if search("|", genes):
                    genes = genes.split("|")
                else:
                    genes = [genes]

                for gene in genes:
                    if gene == "NA":
                        continue
                    dgene = self.NextBio.loadGeneToBodyAtlas(gene)
                    for system in dgene.keys():
                        for organ in dgene[system].keys():
                            if dgeneControl != {}:
                                fold = float(dgene[system][organ]["expression"]) / float(median(dgeneControl[self.dorgan[system][organ]]))
                            else:
                                fold = float(dgene[system][organ]["expression"]) / float(dgene[system][organ]["control"])
                            if fold <= 5 and fold >= 2:
                                dcount[self.dorgan[system][organ]][2] = 1
                            elif fold <= 10 and fold > 5:
                                dcount[self.dorgan[system][organ]][5] = 1
                            elif fold > 10:
                                dcount[self.dorgan[system][organ]][10] = 1

                for organ in dcount.keys():
                    if dcount[organ][10] == 1:
                        dout[organ][10] = dout[organ][10] + 1
                    elif dcount[organ][5] == 1:
                        dout[organ][5] = dout[organ][5] + 1
                    elif dcount[organ][2] == 1:
                        dout[organ][2] = dout[organ][2] + 1


        if dgeneControl != {}:
            pfilout = pr_out + "countAssaysByExp_RefOrganExp"
        else:
            pfilout = pr_out + "countAssaysByExp"
        filout = open(pfilout, "w")
        filout.write("Organ\tFold\tcount\n")
        for organ in dout.keys():
            filout.write("%s\tNone\t%s\n"%(organ, dout[organ]["No"]))
            filout.write("%s\tFold [2,5]\t%s\n"%(organ, dout[organ][2]))
            filout.write("%s\tFold ]5,10]\t%s\n"%(organ, dout[organ][5]))
            filout.write("%s\tFold ]10\t%s\n"%(organ, dout[organ][10]))
        filout.close()
