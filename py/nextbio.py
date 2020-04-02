import requests
from shutil import copyfile, move
from os import path, listdir
import xml.etree.ElementTree as ET
from numpy import median


import pathFolder


class nextbio:
    def __init__(self, prout, pkey="", server_request=0):
        """
        parms:
        - pkey: file with the key to connect to nextbio db
        - server_request: 1 load xml from nextbio DB and 0 if not connection, loaded before
        - prout: path folder output
        """
        self.prout = prout
        self.prXML = pathFolder.createFolder(prout + "XML/")

        # load the keys
        self.key = ""
        if pkey == "":
            if path.exists("./../key_nextbio.txt"):
                pkey = "./../key_nextbio.txt"
        if pkey != "":
            fkey = open(pkey, "r")
            key = fkey.read()
            key=key.strip()
            fkey.close()
            self.key=key
        self.request = server_request


    def writeListOrgan(self):
        """
        Open XML files when it is loaded
        """
        lfilexml = listdir(self.prXML)

        pfilin = self.prXML + lfilexml[0]
        # load XML
        dmap = self.parseGeneXML(pfilin)
        pfilout = self.prout + "list_organ.txt"
        filout = open(pfilout, "w")
        for organ in dmap.keys():
            filout.write("|--" + organ + "\n")
            for suborg in dmap[organ].keys():
                filout.write("    |--" + suborg + "\n")
        filout.close


    def loadGeneToBodyAtlas(self, gene):
        """
        Load gene by gene
        """
        pgenexml = self.prXML + gene.replace("/", "-") + ".xml"
        if path.exists(pgenexml):
            return self.parseGeneXML(pgenexml)
        else:
            if self.request == 0:
                return {}
            with requests.Session() as s:
                resp = s.get("https://niehs.ussc.informatics.illumina.com/c/nbapi/bodyatlas.api?apikey=%s&v=0&fmt=xml&q=%s&bodyatlastype=TISSUE&source=1&bodyatlasview=SYSTEM"%(self.key, gene))
                # result = str(resp)
                resp = str(resp.text)

                fxml = open(pgenexml, "w")
                fxml.write(resp)
                fxml.close()

            # move file
            if path.exists(pgenexml) and path.getsize(pgenexml) > 400:
                return self.parseGeneXML(pgenexml)
            else:
                print ("Error nextBio server request")
                return {}


    def parseGeneXML(self, pxmlin):

        dxml = {}

        treeXML = ET.parse(pxmlin)
        root = treeXML.getroot()

        for nextbioresult in root:
            if nextbioresult.tag == "result":
                for result in nextbioresult:
                    if result.tag == "element":
                        for element in result:
                            #print element.attrib
                            if element.tag == "bodySystem":
                                bodysystem = element.text
                                if not bodysystem in list(dxml.keys()):
                                    dxml[bodysystem] = {}
                            if element.tag == "concepts":
                                for concept in element:
                                    for element2 in concept:
                                        if element2.tag == "conceptLabel":
                                            tissu = element2.text
                                        elif element2.tag == "controlExpression":
                                            control = element2.text
                                        elif element2.tag == "tissueExpression":
                                            expression = element2.text
                                        elif element2.tag == "standardDeviation":
                                            SD = element2.text
                                    if control != "0.0": # manage error in the XML with control to 0.0
                                        CONTROL = control
                                    #else:
                                    #    print(pxmlin)
                                    #    print(tissu)

                                    dxml[bodysystem][tissu] = {}
                                    if control == "0.0":
                                        #print(pxmlin, bodysystem, tissu)
                                        try:dxml[bodysystem][tissu]["control"] = CONTROL
                                        except:dxml[bodysystem][tissu]["control"] = control

                                    else: 
                                        dxml[bodysystem][tissu]["control"] = control
                                    dxml[bodysystem][tissu]["expression"] = expression
                                    dxml[bodysystem][tissu]["SD"] = SD

        self.xml = dxml
        return dxml


    def defineOrganMedExpression(self, dorgan):

        # list of gene
        lfilexml = listdir(self.prXML)

        dout = {}
        for system in dorgan.keys():
            for tissue in dorgan[system].keys():
                organ = dorgan[system][tissue]
                if not organ in dout:
                    dout[organ] = []

        for fileXML in lfilexml:
            dgene = self.parseGeneXML(self.prXML + fileXML)
            for system in dgene.keys():
                for tissue in dgene[system].keys():
                    organ = dorgan[system][tissue]
                    expression = dgene[system][tissue]["expression"]
                    if expression != 'NA':
                        dout[organ].append(float(expression))

        pfilout = self.prout + "conrolByOrgan"
        filout = open(pfilout, "w")
        filout.write("Organ\tcontrol\n")
        for organ in dout.keys():
            filout.write("%s\t%s\n"%(organ, median(dout[organ])))
        filout.close()

        self.geneControlByOrgan = dout

        return dout


