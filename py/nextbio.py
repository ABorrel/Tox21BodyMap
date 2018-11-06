from urllib import urlretrieve
from shutil import copyfile, move
from os import path
import xml.etree.ElementTree as ET

from scipy.signal import bode

import pathFolder


key = "67dfcb212a463142bd17a339927fe3ed"

"https://niehs.ussc.informatics.illumina.com/c/apiTestbed/testbed.nb"


class nextbio:
    def __init__(self, prout):

        self.prXML = pathFolder.createFolder(prout + "XML/")




    def runGeneToBodyAtlas(self, gene):

        pgenexml = self.prXML + gene + ".xml"
        if path.exists(pgenexml):
            self.parseGeneXML(pgenexml)

        else:
            request = ("https://niehs.ussc.informatics.illumina.com/c/nbapi/bodyatlas.api?apikey=67dfcb212a463142bd17a339927fe3ed&v=0&fmt=xml&q=%s&bodyatlastype=TISSUE&source=1&bodyatlasview=SYSTEM"%(gene))

            presult = urlretrieve(request)

            # move file
            move(presult[0], pgenexml)
            if path.exists(pgenexml):
                self.parseGeneXML(pgenexml)
            else:
                print "Error nextBio result"



    def parseGeneXML(self, pxmlin):

        dxml = {}

        treeXML = ET.parse(pxmlin)
        root = treeXML.getroot()

        for nextbioresult in root:
            if nextbioresult.tag == "result":
                for result in nextbioresult:
                    if result.tag == "element":
                        for element in result:
                            print element.tag
                            print element.attrib
                            if element.tag == "bodySystem":
                                print "ddd"
                                print element.text
                                
                                for bodySystem in element:
                                    print bodySystem.tag
                                    print bodySystem.attrib.keys()
                                    print bodySystem.text
                                #print element.tag
                                #print element.attrib



        dddd









