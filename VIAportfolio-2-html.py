#!/usr/bin/python

import os, sys
import re
import lxml.etree
import xml.etree.ElementTree

# cat PoliticalButtons_VIA_portfolio.xml | sed s'/work\.image/workImage/g' | sed s'/work.title/workTitle/g' > PoliticalButtons_VIA_portfolioCLEAN.xml

XML = '/home/comstock/Downloads/PoliticalButtons_VIA_portfolio.xml'
CLEAN ='PoliticalButtons_VIA_portfolioCLEAN.xml'
CNT = 1
target = open("via.html", 'w')
from xml.dom import minidom

doc = minidom.parse(XML)

# doc.getElementsByTagName returns NodeList
name = doc.getElementsByTagName("imagelink")[0]
element = doc.getElementsByTagName("imagelink")
count = len(element)
#print count


line1 = "<html>\
<head>\
   <title>Images from VIA </title>\
   </head>\
   <body>\
   \
   "
target.write(line1)

while CNT < count:
    ##print(name.firstChild.data)
    
    jelly = doc.getElementsByTagName("imagelink")[CNT]
    #print "<img src=\"" + (jelly.firstChild.data) + "\" />"
    line2 = "<img src=\"" + (jelly.firstChild.data) + "\" />"
    target.write(line2)
    #link = doc.getElementsByTagName("imagelink")[CNT]
    #print link
    CNT = CNT + 1
line3 = "</body></html>"
target.write(line3)
