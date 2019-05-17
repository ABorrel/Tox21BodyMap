from urllib import urlretrieve
from shutil import copyfile, move
from os import path
import xml.etree.ElementTree as ET


import pathFolder


key = "67dfcb212a463142bd17a339927fe3ed"

"https://niehs.ussc.informatics.illumina.com/c/apiTestbed/testbed.nb"


class nextbio:
    def __init__(self, prout):

        self.prXML = pathFolder.createFolder(prout + "XML/")




    def runGeneToBodyAtlas(self, gene):

        pgenexml = self.prXML + gene.replace("/", "-") + ".xml"
        if path.exists(pgenexml):
            return self.parseGeneXML(pgenexml)

        else:
            request = ("https://niehs.ussc.informatics.illumina.com/c/nbapi/bodyatlas.api?apikey=67dfcb212a463142bd17a339927fe3ed&v=0&fmt=xml&q=%s&bodyatlastype=TISSUE&source=1&bodyatlasview=SYSTEM"%(gene))

            presult = urlretrieve(request)

            # move file
            if path.exists(presult[0]):
                move(presult[0], pgenexml)
                return self.parseGeneXML(pgenexml)
            else:
                print "Error nextBio result"
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
                                if not bodysystem in dxml.keys():
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

                                    dxml[bodysystem][tissu] = {}
                                    dxml[bodysystem][tissu]["control"] = control
                                    dxml[bodysystem][tissu]["expression"] = expression
                                    dxml[bodysystem][tissu]["SD"] = SD


        return dxml









