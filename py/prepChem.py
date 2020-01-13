import toolbox
import DBrequest

PTOX21CHEMSUM = "/home/borrela2/data/invitroDBV3_2019/INVITRODB_V3_1_SUMMARY/Chemical_Summary_190226.csv"
PTOX21CHEM = "/home/borrela2/BodyMap/data/Tox21_chem.csv"





def prepChemForWebsite(prout, indb =0):

    dTox21ChemSum = toolbox.loadMatrixToDict(PTOX21CHEMSUM, sep = ",")
    dTox21Chem = toolbox.loadMatrixToDict(PTOX21CHEM, sep = '\t')

    #print(dTox21Chem)
    #print(dTox21ChemSum)

    cDB = DBrequest.DBrequest()

    dout = {}
    for chem in dTox21ChemSum:
        CAS = dTox21ChemSum[chem]["casn"]
        dtxid = dTox21ChemSum[chem]["dsstox_substance_id"]
        name = dTox21ChemSum[chem]["chnm"]
        try: SMILES = dTox21Chem[dtxid]["smiles_origin"]
        except: SMILES = 0
        dout[CAS] = {}
        dout[CAS]["DTXID"] = dtxid
        dout[CAS]["name"] = name
        dout[CAS]["SMILES"] = SMILES

    pfilout = prout + "ChemSum"
    filout = open(pfilout, "w")
    filout.write("CAS\tDTXID\tName\tSMILES\n")

    for chem in dout.keys():
        if dout[chem]["SMILES"] == 0:
            continue
        filout.write("%s\t%s\t%s\t%s\n"%(chem, dout[chem]["DTXID"], dout[chem]["name"], dout[chem]["SMILES"]))
        if indb == 1:
            cDB.addElement("bodymap_chemicals", ["casn", "dsstox_id", "name", "smiles"], [chem, dout[chem]["DTXID"], dout[chem]["name"], dout[chem]["SMILES"]])

    filout.close()

    return dout