#!/usr/bin/python
import re
import json
import urllib2
from xml.dom import minidom
from urlparse import urlparse

def catalog_record():
    via_id = doc.getElementsByTagName('via_id')[CNT]
    via_id = via_id.toxml()
    via_id = re.sub("<via_id>","",via_id)
    via_id = re.sub("</via_id>","",via_id)
    return via_id
    
def image_link():
    imgLink = doc.getElementsByTagName('imagelink')[CNT]
    urn = imgLink.toxml()
    urn = re.sub("<imagelink>http://nrs.harvard.edu/","",urn)
    urn =re.sub("</imagelink>","",urn)
    return urn

def pixel_dim(urn):
    webUrl  = urllib2.urlopen(NRS_STEM + urn)
    redir = webUrl.geturl()
    parsed = urlparse(redir)
    ID = parsed.path
    ID = re.sub("\/ids\/view/","",ID)
    
    JSONURL =  urllib2.urlopen(ids_stem + ID + ids_stern)
    # print ids_stem + ID + ids_stern
    data = JSONURL.read()
    theJSON = json.loads(data)
    url = theJSON["@id"]
    url = re.sub("iiif","view",url)
    url = re.sub("http://ids.lib.harvard.edu/ids/view/","",url)
    hw = "(" + str(theJSON["width"]) +" pixels wide x " + str(theJSON["height"]) + " pixels high)"    
    return hw
    
def caption():
    title = doc.getElementsByTagName('record')[CNT]
    title = title.toxml()
    title = re.sub("\n","",title)
    title = re.sub("<record>.*<work.title>.*<text>","",title); title = re.sub("</text>.*","",title)
    return title     

def main():
    ## VARIABLES ##
    # VIA Portfolio Source
    XML = "C:\\temp\portfolio\wilsonTransformed_records.xml"
    global CNT ; CNT = 0
    target = open("20160409.html", 'w')
    portfolio = open(XML, 'r')
    global doc ; doc = minidom.parse(XML)
    element = doc.getElementsByTagName("imagelink")
    count = len(element)
    record_stem = "http://id.lib.harvard.edu/via/"
    record_tail = "/catalog"
    global ids_stem ; ids_stem = 'http://ids.lib.harvard.edu/ids/iiif/'
    global ids_stern ; ids_stern = '/info.json'
    global NRS_STEM ; NRS_STEM = "http://nrs.harvard.edu/"
    html_title = "VIA Images"
    # URN = "urn-3:ARB.JPLIB:695790"

    ## HTML CODE ##
    head = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n\
    <head>\n\
    <!-- <title>Images from VIA </title>\n\ -->\
    <title>" + html_title + "</title>\n\
    <link rel=\"stylesheet\" href=\"http://www.w3.org/StyleSheets/Core/Traditional\" type=\"text/css\" />\n\
    </head>\n\
    <body>\n"
    target.write(head)
   
    while CNT != count:
        via_id = catalog_record()
        urn = image_link()
        title = caption()
        hw = pixel_dim(urn)
  
        body = "\
        <figure>\n\
        <a href=\"http://nrs.harvard.edu/" + urn + "?buttons=y\" target=\"_blank\"><img src=\"http://nrs.harvard.edu/" + urn + "\" alt=\"" + urn + "\"/></a>\n\
        <figcaption>\n\
        <a href=\"" + record_stem + via_id + record_tail + "\" target=\"_blank\">" + title + "</a><br />\n" + hw + "\
        \n</figcaption>\n</figure>\n"
    
        tail = "\
        </body>\
        </html>"
        
        target.write(body)
        print "    wrote line for image " + str(CNT) + " of " + str(count) + "\n"
        
        CNT = CNT + 1
    
    target.write(tail)
    print "\n    ~~~~ FIN ~~~~\n"

if __name__ == "__main__":
    main()
