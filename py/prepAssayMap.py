import toolbox
import DBrequest


class prepAssay:
    def __init__(self, pprepmap):
        self.pprepmap = pprepmap
        self.cDB = DBrequest.DBrequest()
        self.cDB.verbose = 0

    def loadPreMapAssay(self):
        dprepmap = toolbox.loadMatrixToDict(self.pprepmap, ",")
        self.dprepmap = dprepmap


    def getdassaysClean(self):
        
        if not "dprepmap" in self.__dict__:
            self.loadPreMapAssay()
        print(self.dprepmap)

        dout = {}
        for assay in self.dprepmap.keys():
            if self.dprepmap[assay]["Type of body mapping"] == "none":
                continue
            else:
                dout[assay] = self.dprepmap[assay]
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

