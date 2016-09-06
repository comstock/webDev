#!/usr/bin/python
## Take an XML VIA portfolio from Harvard's image catalog
## and return an HTML page that includes displayed images
## where the image links to a zoom-able interface to the image
## and is captioned with the <title> from the catalog record
## where caption-text links to catalog record and is
## followed by a notation of the image pixel dimensions
## for the largest available image stored in the Harvard Library's
## preservation digital repository.
##
# -*- coding: utf-8 -*-
import codecs
import re
import json
import urllib2
from xml.dom import minidom
from urlparse import urlparse

def catalog_record(): # extract catalog record id
    try:
        via_id = doc.getElementsByTagName('via_id')[CNT]
        via_id = via_id.toxml()
        via_id = re.sub("<via_id>","",via_id)
        via_id = re.sub("</via_id>","",via_id)
        return via_id
    except (RuntimeError, TypeError, NameError, IOError, OSError):
        print "VIA ID ERROR"
        via_id = "NONE"
        return via_id
    
def image_link(): # extract URN for image to build link
    try:
        imgLink = doc.getElementsByTagName('imagelink')[CNT]
        urn = imgLink.toxml()
        urn = re.sub("<imagelink>http://nrs.harvard.edu/","",urn)
        urn =re.sub("</imagelink>","",urn)
        return urn
    except (RuntimeError, TypeError, NameError, IOError, OSError):
        print "IMAGE LINK ERROR"
        urn = "NONE"
        return urn

def pixel_dim(urn): # extract size of largest available image
    try:
        webUrl  = urllib2.urlopen(NRS_STEM + urn)
        # The URN redirects to another URL. The following line picks up the URL we are redirected to.
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
        hw = "(Full size image: " + str(theJSON["width"]) +" pixels wide x " + str(theJSON["height"]) + " pixels high)"    
        return hw
    except (RuntimeError, TypeError, NameError, IOError, OSError):
        print "HW ERROR"
        hw = "Failed to retrieve image dimensions from server (sadface)."
        return hw
    
def caption():
    title = doc.getElementsByTagName('record')[CNT]
    title = title.toxml()
##    title = title.encode("utf-8")
    date = title
    creator = title
    # turn record into single-line string to
    # avoid having to deal with line returns
    title = re.sub("\n","",title)
    date = re.sub("\n","",date)
    creator = re.sub("\n","",creator)
    
    title = re.sub("<record>.*<work.title>.*<text>","",title); title = re.sub("</text>.*","",title)
    date = re.sub("<record>.*<work.date>","",date); date = re.sub("</work.date>.*","",date)
    
    # Only populate *creator* if the <work.creator>Name> value is located
    if re.search("<record>.*<work.creator>\s*<name>",creator):
        creator = re.sub("<record>.*<work.creator>\s*<name>","",creator) ;creator = re.sub("</name>.*","",creator)
    else:
        creator =""
    
    if re.search("\d\d\d\d-\d\d-\d\d",date):
        date = re.sub("-\d\d-\d\d","",date)
      
##    print "DATE: " + date + "; " + "CREATOR: " + creator 
    print "DATE: " + date.encode("utf-8") + "; " + "CREATOR: " + creator.encode("utf-8") 
    if creator != "":
        title = title + " [" + date + "]<br />" + creator
    else:
        title = title + " [" + date + "]<br />"
    return title     

def main():
    ## VARIABLES ##
    # VIA Portfolio Sourcework.
    XML = "/home/comstock/Documents/Transformed_records.xml"
    global CNT ; CNT = 0
    # open HTML file for writing output
    target = open("Welch_20160906.html", 'w')
    portfolio = open(XML, 'r')
    global doc ; doc = minidom.parse(XML)
    element = doc.getElementsByTagName("record")
    count = len(element)
    
    # To limit number of records returned, uncommment the following 4 lines.
##    if count > 100:
##        count = 100
##    else:
##        count = count
    
    record_stem = "http://id.lib.harvard.edu/via/"
    record_tail = "/catalog"
    global ids_stem ; ids_stem = 'http://ids.lib.harvard.edu/ids/iiif/'
    global ids_stern ; ids_stern = '/info.json'
    global NRS_STEM ; NRS_STEM = "http://nrs.harvard.edu/"
    #global creator # ; creator = "ERROR: No <work.creator><name> value found."
    # <title> of HTML page
    html_title = "VIA Images, SC Welch"
    # URN = "urn-3:ARB.JPLIB:695790"

    ## HTML CODE ##
    head = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
    <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n\
    \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n\
    <html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n\
    <head>\n\
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
        <a href=\"" + record_stem + via_id + record_tail + "\" target=\"_blank\">" + title + "</a><br />" + hw + "<br />\n\
        </figcaption>\n\
        </figure>\
        \n\n"
        
        body = body.encode("utf-8")
    
        tail = "\
        </body>\
        </html>"
        
        target.write(body)
        print "    wrote entry for image " + str(CNT + 1) + " of " + str(count) + "\n"      
        CNT = CNT + 1
    
    target.write(tail)
    print "\n    ~~~~ FIN ~~~~\n"

if __name__ == "__main__":
    main()
