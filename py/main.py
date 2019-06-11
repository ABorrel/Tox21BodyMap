import ToxCast
import pathFolder
import nextbio
import mapGeneToBody
import mapChem
import mapAssays


PR_ROOT = "/home/borrela2/BodyMap/"
PR_MAPPING = PR_ROOT + "MAPPING/"


#ToxCast
PTOXCAST_ASSAYS = PR_ROOT + "data/ToxCast/ToxCast_assay_master_2017-06-14.csv"
PTOXCAST_AC50 = PR_ROOT + "data/ToxCast/ac50_Matrix_170614.csv"
PTOXCAST_CHEM = PR_ROOT + "data/ToxCast/toxcast_chemicals_2017-06-14.csv"




###########
# TOXCast #
###########
prToxCast = pathFolder.createFolder(PR_MAPPING + "ToxCast/")
TC = ToxCast.ToxCast(PTOXCAST_CHEM, PTOXCAST_AC50, PTOXCAST_ASSAYS, prToxCast)

# => Assays
TC.loadAssays()

###########
# NEXTBio # => download
###########
PR_NEXTBIO = pathFolder.createFolder(PR_ROOT + "data/NEXTBIO/")
NB = nextbio.nextbio(PR_NEXTBIO)




###########################
# MAP gene body => nextbio #
###########################
prToxCastVsBody = pathFolder.createFolder(PR_MAPPING + "GeneToxCastVSBody/")
cGeneToBody = mapGeneToBody.MapGeneToBody(TC, NB, 0, prToxCastVsBody)
cGeneToBody.mapGene()
#cGeneToBody.refineMappingWithExp(2)
#cGeneToBody.refineMappingWithExp(5)



###########################
# Mapping assays to body  #
###########################
lexcluded = ["NHEERL_HUNTER", "NHEERL_SHAFER", "STEMINA", "TANGUAY"]
cassays = mapAssays.mapAssays(cGeneToBody, TC, NB, PR_MAPPING)
cassays.map(5, lexcluded)



sss



#############
#  by Chem  #
#############

TC.loadChem()
TC.loadAC50()


##################
# maping Chem on #
##################
prChem = pathFolder.createFolder(PR_MAPPING + "Chem/")
cmapChem = mapChem.mapChem(TC, cGeneToBody, prChem)

cmapChem.map()