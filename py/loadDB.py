import DBrequest




def uploadAC50InDB(TC, nametable):

        cDB = DBrequest.DBrequest()
        lassays = list(TC.dassays.keys())

        for chem in TC.dchem.keys():
            for assay in lassays:
                if assay in list(TC.dchem[chem].activeAssays.keys()):
                    cDB.addElement(nametable, ["casn", "ac50", "assay"], [chem, TC.dchem[chem].activeAssays[assay], assay])
                    

