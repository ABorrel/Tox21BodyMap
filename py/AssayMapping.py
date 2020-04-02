import toolbox
import DBrequest
import pathFolder
import runExtScript


class prepAssay:
    def __init__(self, pprepmap):
        self.pprepmap = pprepmap
        self.cDB = DBrequest.DBrequest()
        self.cDB.verbose = 0
        self.error = 0


    def loadPreMapAssay(self):
        dprepmap = toolbox.loadMatrixToDict(self.pprepmap, ",")
        self.dprepmap = dprepmap


    def getdassaysClean(self):
        
        if not "dprepmap" in self.__dict__:
            self.loadPreMapAssay()

        dout = {}
        for assay in self.dprepmap.keys():
            if self.dprepmap[assay]["Type of body mapping"] == "none":
                continue
            else:
                dout[assay] = self.dprepmap[assay]

        self.dprepmapclean = dout 
        return dout

    def pushAssayMapInDB(self, nameTable):

        for assay in self.dprepmap.keys():
            if self.dprepmap[assay]["Type of body mapping"] == "none":
                continue
            
            if self.dprepmap[assay]["Type of body mapping"] == "tissue":
                if self.dprepmap[assay]["Tissue"] == "liver":
                    organ = "Liver"
                    system = "Digestive System"
                elif self.dprepmap[assay]["Tissue"] == "vascular":
                    organ = "Vascular"
                    system = "Cardiovascular System"
                elif self.dprepmap[assay]["Tissue"] == "lung":
                    organ = "Lung"
                    system = "Respiratory System"
                elif self.dprepmap[assay]["Tissue"] == "skin":
                    organ = "Skin"
                    system = "Integumentary System"
                elif self.dprepmap[assay]["Tissue"] == "thyroid gland":
                    organ = "Thyroid gland"
                    system = "Endocrine System" 
                elif self.dprepmap[assay]["Tissue"] == "cervix":
                    organ = "Uterus"
                    system = "Urogenital System" 
                else:
                    print(self.dprepmap[assay]["Tissue"])
                    dddd
                self.cDB.addElement(nameTable, ["assay", "type_map", "organ", "system"], [assay, "tissue", organ, system])
            
            elif self.dprepmap[assay]["Type of body mapping"] == "viability":
                self.cDB.addElement(nameTable, ["assay", "type_map"], [assay, "viability"])
            
            elif self.dprepmap[assay]["Type of body mapping"] == "gene target":
                gene = self.dprepmap[assay]["Gene"]
                if gene == "NA":
                    continue

                self.cDB.addElement(nameTable, ["assay", "type_map", "gene"], [assay, "gene", gene])
    
    def summaryMapping(self, pr_out):

        if not "dprepmapclean" in self.__dict__:
            print("ERROR loading mapping")
            self.error = 1
            return 1

        # create directory in results
        pr_out = pathFolder.createFolder(pr_out + "sum_assays/")        
        pfilout = pr_out + "count_mapping"
        filout = open(pfilout, "w")
        filout.write("Assay\tType of organ mapping\n")

        for assay in list(self.dprepmapclean.keys()):
            if self.dprepmapclean[assay]["Type of body mapping"] == "viability":
                filout.write("%s\tViability\n"%(assay))
            elif self.dprepmapclean[assay]["Type of body mapping"] == "gene target":
                filout.write("%s\tGene target\n"%(assay))
            elif self.dprepmapclean[assay]["Type of body mapping"] == "tissue":
                filout.write("%s\tCell type\n"%(assay))
        filout.close()

        # add R script
        runExtScript.histAssayMapping(pfilout)