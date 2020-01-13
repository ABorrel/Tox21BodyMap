import pathFolder
import nextbio
import mapAssaysToBody
import mapChem
import mapAssays
import prepAssayMap
import prepChem
import DBrequest


#=> to import ToxCast librairy
import sys
sys.path.insert(0, "/home/borrela2/development/ToxCastlib/py/")
import ToxCast



def uploadAC50InDB(TC, nametable):

        cDB = DBrequest.DBrequest()
        lassays = list(TC.dassays.keys())

        for chem in TC.dchem.keys():
            for assay in lassays:
                if assay in list(TC.dchem[chem].activeAssays.keys()):
                    cDB.addElement(nametable, ["casn", "ac50", "assay"], [chem, TC.dchem[chem].activeAssays[assay], assay])
                    



PR_ROOT = "/home/borrela2/BodyMap/"
PR_MAPPING = PR_ROOT + "MAPPING/"

porgan = PR_ROOT + "data/organ_mapping_final.csv"
passaysmapping = PR_ROOT + "data/AssaysMappingType_final.csv"

# load interest assays
prep = prepAssayMap.prepAssay(passaysmapping)
dassays_premap = prep.getdassaysClean()
prep.pushAssayMapInDB("bodymap_assay_mapping_new")
dddd

###########
# TOXCast #
###########
prToxCast = pathFolder.createFolder(PR_MAPPING + "ToxCast/")
TC = ToxCast.ToxCast([], prToxCast)

# => Assays
TC.loadAssays(list(dassays_premap.keys()))

# => chemical
TC.loadChem()
TC.loadAC50()
#TC.writebyChemical(prToxCast) # wrtie chem by chem
#uploadAC50InDB(TC, "bodymap_assay_ac50")

######
# create chemical table for website
prchem = pathFolder.createFolder(PR_ROOT + "chemWebsite/")
prepChem.prepChemForWebsite(prchem, indb=1)
sss

###########
# NEXTBio # => download
###########
PR_NEXTBIO = pathFolder.createFolder(PR_ROOT + "data/NEXTBIO/")
NB = nextbio.nextbio(PR_NEXTBIO)
#NB.writeListOrgan()


###########################
# MAP gene body => nextbio #
###########################
#prToxCastVsBody = pathFolder.createFolder(PR_MAPPING + "AssaysToxCastVSBody/")
#cAssayToBody = mapAssaysToBody.MapAssaysToBody(TC, NB, porgan, 0, prToxCastVsBody)
#cAssayToBody.premapAssays(dassays_premap)
#cAssayToBody.getGeneExpression(inDB = 1)
#cGeneToBody.mapGene()

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





##################
# maping Chem on # ==> no really usefull because the mapping can be
##################
#prChem = pathFolder.createFolder(PR_MAPPING + "Chem/")
#cmapChem = mapChem.mapChem(TC, cGeneToBody, prChem)
#cmapChem.map()




# push