from os import system, path
from shutil import copy
from copy import deepcopy

def selectMinimalEnergyLigPrep(psdfin, psdfout):

    # case of only one
    filin = open(psdfin, "r")
    readfile = filin.read()
    filin.close()

    lsdf = readfile.split("$$$$\n")[:-1]


    if len(lsdf) == 1:
        copy(psdfin, psdfout)

    else:
        #find with the lower energy
        lenergy = []
        for sdfin in lsdf:
            energy = sdfin.split("> <r_lp_Energy>\n")[-1].split("\n")[0]
            print energy
            lenergy.append(float(energy))

        # take minimal energy
        ibest = lenergy.index(min(lenergy))
        filout = open(psdfout, "w")
        filout.write(lsdf[ibest] + "$$$$\n")
        filout.close()

    return psdfout



def renameHeaderSDF(pfilin):
    """Rename header with name file"""
    namesdf = pfilin.split("/")[-1].split(".")[0]
    filin = open(pfilin, "r")
    llines = filin.readlines()
    filin.close()
    llines[0] = str(namesdf) + "\n"

    filout = open(pfilin, "w")
    filout.write("".join(llines))
    filout.close()

import multiprocessing
import time

def timeFunction(funct, mol):

    manager = multiprocessing.Manager()
    lout = manager.list()

    p = multiprocessing.Process(target=funct, args=(mol, lout))
    p.start()
    time.sleep(2)

    if p.is_alive():
        p.terminate()
        p.join()
        return "ERROR"
    else:
        p.join()
        #print lout
        return lout[0]


from scipy import stats
from numpy import delete
def rankList(lin):

    liNA =  [i for i,x in enumerate(lin) if x == 'NA']
    linWithoutNA = deepcopy(lin)
    linWithoutNA = delete(linWithoutNA, liNA).tolist()


    linWithoutNA = [float(i) for i in linWithoutNA]
    n = len(linWithoutNA)

    lrank = stats.rankdata(linWithoutNA)
    lrank = [int(abs(i-n)) for i in lrank]

    for i in liNA:
        lrank.insert(i, "NA")

    return lrank


def loadMatrixToDict(pmatrixIn, sep ="\t"):

    filin = open(pmatrixIn, "r")
    llinesMat = filin.readlines()
    filin.close()

    dout = {}
    line0 = formatLine(llinesMat[0])
    line1 = formatLine(llinesMat[1])
    lheaders = line0.split(sep)
    lval1 = line1.split(sep)

    # case where R written
    if len(lheaders) == (len(lval1)-1):
        lheaders.append("val")

    i = 1
    imax = len(llinesMat)
    while i < imax:
        lineMat = formatLine(llinesMat[i])
        lvalues = lineMat.split(sep)
        kin = lvalues[0]
        dout[kin] = {}
        j = 0
        if len(lvalues) != len(lheaders):
            print "Error => nb element"
            print len(lvalues)
            print len(lheaders)

        jmax = len(lheaders)
        while j < jmax:
            dout[kin][lheaders[j]] = lvalues[j]
            j += 1
        i += 1

    return dout




def loadMatrixToList(pfilin, sep = "\t"):

    lout = []

    filin = open(pfilin, "r")
    llines = filin.readlines()
    filin.close()

    lheader = llines[0].strip().split(sep)
    nbheader = len(lheader)

    for linei in llines[1:]:
        linei = formatLine(linei)
        lelem = linei.strip().split(sep)
        i = 0
        dtemp = {}
        while i < nbheader:
            dtemp[lheader[i]] = lelem[i]
            i += 1

        lout.append(dtemp)

    return lout




def formatLine(linein):

    linein = linein.strip()
    linenew = ""

    imax = len(linein)
    i = 0
    flagchar = 0
    while i < imax:
        if linein[i] == '"' and flagchar == 0:
            flagchar = 1
        elif linein[i] == '"' and flagchar == 1:
            flagchar = 0

        if flagchar == 1 and linein[i] == ",":
            linenew = linenew + " "
        elif flagchar == 1 and linein[i] == "\n":
            linenew = linenew + " "
        else:
            linenew = linenew + linein[i]
        i += 1

    linenew = linenew.replace('\"', "")
    return linenew






def writeMatrix(ddesc, pdescAct, sep = "\t"):


    filout = open(pdescAct, "w")
    lheader = ddesc[ddesc.keys()[0]].keys()

    # put header in first

    if "CAS" in lheader:
        del lheader[lheader.index("CAS")]
        lheader = ["CAS"] + lheader
    elif "CASID" in lheader:
        del lheader[lheader.index("CASID")]
        lheader = ["CASID"] + lheader
    else:
        lheader = ["CASID"] + lheader
        for casID in ddesc.keys():
            ddesc[casID]["CASID"] = casID


    filout.write(sep.join(lheader) + "\n")
    for casID in ddesc.keys():
        lval = [str(ddesc[casID][i]) for i in lheader]
        filout.write(sep.join(lval) + "\n")
    filout.close()



def loadSMILES(psmi):


    filin = open(psmi, "r")
    smiles = filin.readlines()[0]
    smiles.strip()
    filin.close()

    return smiles




