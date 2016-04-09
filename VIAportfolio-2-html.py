#!/usr/bin/python
#import os, sys
import re
import json
import urllib2
from xml.dom import minidom
from urlparse import urlparse

# VIA Portfolio Source
XML = "C:\\temp\portfolio\Transformed_records.xml"
CNT = 1
target = open("20160402.html", 'w')
portfolio = open(XML, 'r')
doc = minidom.parse(XML)
element = doc.getElementsByTagName("imagelink")
count = len(element)
record_stem = "http://id.lib.harvard.edu/via/"
record_tail = "/catalog"
ids_stem = 'http://ids.lib.harvard.edu/ids/iiif/'
ids_stern = '/info.json'
NRS_STEM = "http://nrs.harvard.edu/"
# URN = "urn-3:ARB.JPLIB:695790"

#print "IMAGELINK COUNT = " + str(count)

# WRITE HTML HEADER TO FILE
head = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n\
<head>\n\
<title>Images from VIA </title>\n\
<link rel=\"stylesheet\" href=\"http://www.w3.org/StyleSheets/Core/Traditional\" type=\"text/css\" />\n\
</head>\n\
<body>\n"
target.write(head)

tail ="\
</body>\
</html>"

while CNT != count:
    imgLink = doc.getElementsByTagName('imagelink')[CNT]
    title = doc.getElementsByTagName('work.title')[CNT]
    via_id = doc.getElementsByTagName('via_id')[CNT]
    via_id = via_id.toxml()
    via_id = re.sub("<via_id>","",via_id)
    via_id = re.sub("</via_id>","",via_id)
    # print "VIA ID: " + str(via_id)
    title = title.toxml()
    title = re.sub("<work.title>","",title)
    title = re.sub("</work.title>","",title)
    title = re.sub("<text>","",title)
    title = re.sub("</text>","",title)

 

    #urn = imgLink.toprettyxml()
    urn = imgLink.toxml()
    urn = re.sub("<imagelink>http://nrs.harvard.edu/","",urn)
    urn =re.sub("</imagelink>","",urn)
    #target.write(urn)
    #target.write("\n")
    #webUrl = urllib2.urlopen("http://ids.lib.harvard.edu/ids/iiif/11869105/info.json")
    webUrl  = urllib2.urlopen(NRS_STEM + urn)
    redir = webUrl.geturl()
    parsed = urlparse(redir)
    ID = parsed.path
    ID = re.sub("\/ids\/view/","",ID)
    # print ID

    JSONURL =  urllib2.urlopen(ids_stem + ID + ids_stern)
    # print ids_stem + ID + ids_stern
    data = JSONURL.read()# get the result code and print it
    theJSON = json.loads(data)

    url = theJSON["@id"]
    url = re.sub("iiif","view",url)
    url = re.sub("http://ids.lib.harvard.edu/ids/view/","",url)

    hw = "(" + str(theJSON["width"]) +" pixels wide x " + str(theJSON["height"]) + " pixels high)"    

    URL = NRS_STEM + "/" + urn


    img_html = "\
<figure>\n\
<a href=\"http://nrs.harvard.edu/" + urn + "?buttons=y\" target=\"_blank\"><img src=\"http://nrs.harvard.edu/" + urn + "\" alt=\"" + urn + "\"/></a>\n\
<figcaption>\n\
<a href=\"" + record_stem + via_id + record_tail + "\">" + title + "</a><br />\n" + hw + "\
\n</figcaption>\n</figure>\n"
    print img_html
    target.write(img_html)
    CNT = CNT + 1

target.write(tail)
