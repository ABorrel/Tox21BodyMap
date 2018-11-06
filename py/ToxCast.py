from re import finditer, escape
from os import path

import Assays
import ChemCAS
import toolbox


def fromatLineAssays(llinesAssays):

    flagopen = 0
    lout = []
    ltemp = []
    for lineAssays in llinesAssays[1:]:
        i = 0
        imax = len(lineAssays)
        itemp = 0
        while i < imax:
            if lineAssays[i] == "," and flagopen == 0:
                ltemp.append(str(lineAssays[itemp:i]))
                itemp = i + 1 # remove coma
            elif lineAssays[i] == "\"" and flagopen == 0:
                flagopen = 1
            elif lineAssays[i] == "\"" and flagopen == 1:
                flagopen = 0
            i += 1

        if len(ltemp) == 80:
            ltemp.append(str(lineAssays[itemp:imax-1]))
            lout.append(ltemp)
            ltemp = []

    return lout




class ToxCast:

    def __init__(self, pchem, pAC50, passays, prresults):

        self.pchem = pchem
        self.pAC50 = pAC50
        self.passays = passays
        self.prresults = prresults


    def loadAssays(self):

        fassays = open(self.passays, "r")
        lsassays = fassays.readlines()
        fassays.close()

        #lclass = lsassays[0].strip().split(",")
        #print(len(lclass))
        #print(lclass)
        lassays = fromatLineAssays(lsassays)

        dout = {}
        for assay in lassays:
            nameAssay = assay[0]
            dout[nameAssay] = Assays.Assay(assay)
        self.dassays = dout



    def loadChem(self):


        self.dchem = {}

        fchem = open(self.pchem, "r")
        lchem = fchem.readlines()
        fchem.close()


        for chem in lchem[1:]:
            # format to split on comma
            lsplit = chem.strip().split(",")
            chemID = lsplit[0]
            casrn = lsplit[1]
            name = ",".join(lsplit[2:])
            self.dchem[casrn] = ChemCAS.ChemCAS(casrn, chemID, name, "")


    def loadChemSpFilter(self, lsourceAssays, cutoffActive):

        pfilout = self.prresults + "chem_" + "-".join(lsourceAssays) + "_" + str(cutoffActive)


        if not "dchem" in self.__dict__:
            self.loadChem()
            self.loadAC50()

        i = 0
        lcas = self.dchem.keys()
        imax = len(lcas)
        while i < imax:
            nactive = 0
            nassays = 0
            ninactive = 0
            if not "activeAssays" in self.dchem[lcas[i]].__dict__:
                del self.dchem[lcas[i]]
                i = i + 1
                continue

            for assays in self.dchem[lcas[i]].activeAssays.keys():
                source = assays.split("_")[0]
                if source in lsourceAssays:
                    nactive = nactive + 1
                    nassays = nassays + 1

            for assays in self.dchem[lcas[i]].notestAssays + self.dchem[lcas[i]].inactiveAssays:
                source = assays.split("_")[0]
                if source in lsourceAssays:
                    nassays = nassays + 1

            for assays in self.dchem[lcas[i]].inactiveAssays :
                source = assays.split("_")[0]
                if source in lsourceAssays:
                    ninactive = ninactive + 1
                    nassays = nassays + 1

            percentageAct = float(nactive + ninactive)/float(nassays)*100.0
            #print nassays, nactive, percentageAct
            if percentageAct < cutoffActive:
                del self.dchem[lcas[i]]
            i = i + 1

        filout = open(pfilout, "w")
        lassays = self.dchem[self.dchem.keys()[0]].notestAssays + self.dchem[self.dchem.keys()[0]].inactiveAssays +\
                  self.dchem[self.dchem.keys()[0]].activeAssays.keys()
        filout.write("CAS\t" + "\t".join(lassays) + "\n")
        for CASID in self.dchem.keys():
            filout.write(CASID)
            for assays in lassays:
                if assays in self.dchem[CASID].activeAssays.keys():
                    filout.write("\t" + str(self.dchem[CASID].activeAssays[assays]))
                elif assays in self.dchem[CASID].inactiveAssays:
                    filout.write("\t1000000")
                elif assays in self.dchem[CASID].notestAssays:
                    filout.write("\tNA")
            filout.write("\n")
        filout.close()


    def loadAC50(self):

        fAC50 = open(self.pAC50, "r")
        lchemIC50 = fAC50.readlines()
        fAC50.close()

        lassays = lchemIC50[0].strip().split(",")

        for chemIC50 in lchemIC50[1:]:
            lChemIC50 = chemIC50.strip().split(",")
            chemID = lChemIC50[0]
            CASID = self.convertIDtoCAS(chemID)

            if CASID != "ERROR":
                self.dchem[CASID].setIC50(lassays, lChemIC50)

    def convertIDtoCAS(self, chemID):

        if not "dchem" in self.__dict__:
            self.loadChem()

        for CASID in self.dchem.keys():
            if self.dchem[CASID].ChemID == chemID:
                return CASID
        return "ERROR"