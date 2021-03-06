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
PR_ROOT = "./../" # have to be change
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
cassayMapped.summaryMapping(PR_RESULTS)

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


#################
# Define control based on organ
#################
dOrganExp = NB.defineOrganMedExpression(dorgan)


#############
# map assay to organ
#############
cmapAssaysToBody = mapAssaysToBody.mapAssaysToBody(NB, dassays_premap, dorgan, PR_RESULTS)
cmapAssaysToBody.analyseCountAssaysByExp()
cmapAssaysToBody.analyseCountAssaysByExp(dOrganExp)





###########
# load ToxCast 
###########

prToxCast = pathFolder.createFolder(PR_RESULTS + "ToxCast_prep/")
TC = ToxCast.ToxCast([], prToxCast)

# => Assays loading
dassays_loaded = TC.loadAssays(list(dassays_premap.keys()))

# => analysis assays by prop
cassayMapped.summaryMappingWithTox21Prop(dassays_loaded, PR_RESULTS)



# => assays in DB with chem and AC50
if PUSH_DB == 1:
    TC.loadChem()
    TC.loadAC50()
    uploadAC50InDB(TC, "bodymap_assay_ac50") # change the table name

    # create file for check
    prchem = pathFolder.createFolder(PR_RESULTS + "chemForDB/")
    prepChem.prepChemForWebsite(prchem, indb=1)
    





