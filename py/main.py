import pathFolder
import nextbio
import mapAssaysToBody
import mapChem
import AssayMapping
import loadInDB
import toolbox


#=> to import ToxCast librairy
import sys
#sys.path.insert(0, "/home/borrela2/development/ToxCastlib/py/")
sys.path.insert(0, "C:/Users/Aborrel/research/NIEHS/development/ToxCastlib/py/") # for window dev
import ToxCast

########
# param 
########
#PR_ROOT = "/home/borrela2/BodyMap/"
PR_ROOT = "C:/Users/Aborrel/research/NIEHS/BodyMap/"
PR_RESULTS = PR_ROOT + "RESULTS/"

# expert driven mapping
porgan = PR_ROOT + "data/organ_mapping_final.csv"
passaysmapping = PR_ROOT + "data/AssaysMappingType_final.csv" #Expert driven approach for mapping

# to push in Database 1 => push in a database already create and defined in a database.ini file on the root
PUSH_DB = 0

#############
# load interest assays
#############
cassayMapped = AssayMapping.AssayMappping(passaysmapping)
dassays_premap = cassayMapped.getdassaysClean()
if PUSH_DB == 1:
    cassayMapped.pushAssayMapInDB("bodymap_assay_mapping_new")

# analyze assays selected
#cassayMapped.summaryMapping(PR_RESULTS)

####################
# load organ mapping on system - manual mapping to limit tissues
####################
dorgan = toolbox.loadOrgan(porgan)


###########
# NEXTBio # => download
###########
PR_NEXTBIO = pathFolder.createFolder(PR_ROOT + "data/NEXTBIO/")
NB = nextbio.nextbio(PR_NEXTBIO)
if PUSH_DB == 1:
    NB.writeListOrgan() # to write the list of organ considered
    loadInDB.uploadGeneExpInDB(dassays_premap, NB, dorgan, PR_RESULTS, w=1)
ddd

#############
# map assay to organ
#############
cmapAssaysToBody = mapAssaysToBody.mapAssaysToBody()


###########
# load ToxCast 
###########

prToxCast = pathFolder.createFolder(PR_RESULTS + "ToxCast_prep/")
TC = ToxCast.ToxCast([], prToxCast)

# => Assays
TC.loadAssays(list(dassays_premap.keys()))

# => assays in DB
TC.loadChem()
TC.loadAC50()
if PUSH_DB == 1:
    uploadAC50InDB(TC, "bodymap_assay_ac50") # change the table name

# => chem in DB
# create chemical table for website => not to use
if PUSH_DB == 1:
    prchem = pathFolder.createFolder(PR_RESULTS + "chemForDB/")
    prepChem.prepChemForWebsite(prchem, indb=1)





# can be del !!!!

###########################
# MAP gene body => nextbio #
###########################
#prToxCastVsBody = pathFolder.createFolder(PR_RESULTS + "AssaysToxCastVSBody/")
#cAssayToBody = mapAssaysToBody.MapAssaysToBody(TC, NB, porgan, 0, prToxCastVsBody)
#cAssayToBody.premapAssays(dassays_premap)
#cAssayToBody.getGeneExpression(inDB = 1)
#cGeneToBody.mapGene()

#cGeneToBody.refineMappingWithExp(2, PR_RESULTS)
#cGeneToBody.refineMappingWithExp(5, PR_RESULTS)