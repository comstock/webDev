#!/usr/bin/python
#-*- coding: utf-8 -*-
import codecs
import os, sys
import re
import time
import pysed
import untangle
#import xmltodict
import lxml.etree
import xml.etree.ElementTree

# cat PoliticalButtons_VIA_portfolio.xml | sed s'/work\.image/workImage/g' | sed s'/work.title/workTitle/g' > PoliticalButtons_VIA_portfolioCLEAN.xml

XML = '/home/comstock/Downloads/PoliticalButtons_VIA_portfolio.xml'
CLEAN ='PoliticalButtons_VIA_portfolioCLEAN.xml'
CNT = 1

from xml.dom import minidom

doc = minidom.parse(XML)

# doc.getElementsByTagName returns NodeList
name = doc.getElementsByTagName("imagelink")[0]
element = doc.getElementsByTagName("imagelink")
count = len(element)
#print count

print "<html>\
<head>\
   <title>Images from VIA </title>\
   </head>\
   <body>\
   \
   "

while CNT < count:
    ##print(name.firstChild.data)

    
    
    
    jelly = doc.getElementsByTagName("imagelink")[CNT]
    print "<img src=\"" + (jelly.firstChild.data) + "\" />"
    #print name.childNodes[1].nodeValue[CNT]
    #print CNT
    #print "title =" + name.getElementsByTagName( 'imagelink' )[0].firstChild.data

    link = doc.getElementsByTagName("imagelink")[CNT]
    #print link
    CNT = CNT + 1
print "</body></html>"
