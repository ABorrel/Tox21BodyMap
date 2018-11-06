


class ChemCAS:

    def __init__(self, CASID, chemID, name, origin):

        self.CASID = CASID
        self.name = name
        self.ChemID = chemID
        self.origin = origin



    def setIC50(self, lassays, lIC50):


        i = 1
        imax = len(lassays)
        lnotest = []
        dactive = {}
        linactive = []

        while i < imax:

            AC50 = lIC50[i]
            if AC50 == "NA":
                lnotest.append(lassays[i])
            elif AC50 == "1e+06":
                linactive.append(lassays[i])
            else:
                dactive[lassays[i]] = AC50

            i += 1

        self.activeAssays = dactive
        self.notestAssays = lnotest
        self.inactiveAssays = linactive



    def ratioActiveAssays(self, typeofCharac, cAssays):


        lcharac = cAssays.getlistCharac(typeofCharac)

        #print(lcharac)
        #print(cAssays.dassays.keys())

        dout = {}
        for charac in lcharac:
            dout[charac] = {"active":0, "inactive":0, "notest":0}

        if not "activeAssays" in self.__dict__:
            self.enrich = {}
            return

        for actAssays in self.activeAssays.keys():
            #print(cAssays.dassays[actAssays].charac[typeofCharac], "DDDD")
            charac = cAssays.dassays[actAssays].charac[typeofCharac]
            dout[charac]["active"] = dout[charac]["active"] + 1

        for inactAssays in self.inactiveAssays:
            charac = cAssays.dassays[inactAssays].charac[typeofCharac]
            dout[charac]["inactive"] = dout[charac]["inactive"] + 1

        for notest in self.notestAssays:
            charac = cAssays.dassays[notest].charac[typeofCharac]
            dout[charac]["notest"] = dout[charac]["notest"] + 1

        self.enrich = {}
        self.enrich[typeofCharac] = dout
