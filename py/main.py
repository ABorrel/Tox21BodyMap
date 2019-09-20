import pathFolder
import nextbio
import mapGeneToBody
import mapChem
import mapAssays



#=> to import ToxCast librairy
import sys
sys.path.insert(0, "/home/borrela2/development/ToxCastlib/py/")
import ToxCast



PR_ROOT = "/home/borrela2/BodyMap/"
PR_MAPPING = PR_ROOT + "MAPPING/"


###########
# TOXCast #
###########
#prToxCast = pathFolder.createFolder(PR_MAPPING + "ToxCast/")
#TC = ToxCast.ToxCast([], prToxCast)

# => Assays
#TC.loadAssays()


###########
# NEXTBio # => download
###########
PR_NEXTBIO = pathFolder.createFolder(PR_ROOT + "data/NEXTBIO/")
NB = nextbio.nextbio(PR_NEXTBIO)
NB.writeListOrgan()
eee

###########################
# MAP gene body => nextbio #
###########################
prToxCastVsBody = pathFolder.createFolder(PR_MAPPING + "GeneToxCastVSBody/")
cGeneToBody = mapGeneToBody.MapGeneToBody(TC, NB, 0, prToxCastVsBody)
cGeneToBody.mapGene()

#cGeneToBody.refineMappingWithExp(2, PR_MAPPING)
#cGeneToBody.refineMappingWithExp(5, PR_MAPPING)



###########################
# Mapping assays to body  #
###########################
lexcluded = ["NHEERL_HUNTER", "NHEERL_SHAFER", "STEMINA", "TANGUAY"]
cassays = mapAssays.mapAssays(cGeneToBody, TC, NB, PR_MAPPING)
cassays.map(2, lexcluded)
#cassays.map(5, lexcluded)
ddd

#############
#  by Chem  #
#############
TC.loadChem()
TC.loadAC50()
TC.writebyChemical(prToxCast)



##################
# maping Chem on # ==> no really usefull because the mapping can be
##################
#prChem = pathFolder.createFolder(PR_MAPPING + "Chem/")
#cmapChem = mapChem.mapChem(TC, cGeneToBody, prChem)
#cmapChem.map()