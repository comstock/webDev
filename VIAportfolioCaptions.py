#!/usr/bin/python
#import os, sys
import re
from xml.dom import minidom

XML = '/home/comstock/Documents/20160323_Transformed_records.xml'
CNT = 1
target = open("20160323.html", 'w')
portfolio = open(XML, 'r')
doc = minidom.parse(XML)
element = doc.getElementsByTagName("imagelink")
count = len(element)
record_stem = "http://id.lib.harvard.edu/via/"
record_tail = "/catalog"
print "IMAGELINK COUNT = " + str(count)

#title = doc.getElementsByTagName('work.title')
#record = doc.getElementsByTagName('via_id')

line1 = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n\
<head>\n\
   <title>Images from VIA </title>\n\
		<link rel=\"stylesheet\" href=\"http://www.w3.org/StyleSheets/Core/Traditional\" type=\"text/css\" />\n\
   </head>\n\
   <body>\n"
target.write(line1)

#via_port = portfolio.readlines()

#for line in via_port:
for line in portfolio:
    #print line
    if re.search(".*<via_id>olvwork*",line):
        line = re.sub("<via_id>","",line)
        line = re.sub("\s","",line)
        line = re.sub("</via_id>","",line)
        line3 = "<a href=\"" + record_stem + line + record_tail + "\" target=\"_blank\">" + line + "</a><hr />"
        #print line3
    elif re.search(".*<group.subwork.component_id>.*",line):
        line = re.sub("<group.subwork.component_id>","",line)
        line = re.sub("\s","",line)
        line = re.sub("</group.subwork.component_id>","",line)
        line3 = "<a href=\"" + record_stem + line + record_tail + "\" target=\"_blank\">" + line + "</a><hr />"

    elif re.search("<group.subwork.image><imagelink>.*", line):
        #line = portfolio.next()
        line = re.sub("<group.subwork.image><imagelink>","",line)
        line = re.sub("</imagelink.*\n","",line)
        #print line
        #line2 = "<figure>\n<img src=\"" + line + "\" />\n"
        line2 = "<figure>\n<a href=\"" + line + "?buttons=y \"target=\"_blank\"><img src=\"" + line + "\"></a>\n"
        target.write(line2)
        
    elif re.search("<work.image><imagelink.*", line):
        #line = portfolio.next()
        line = re.sub("<work.image><imagelink>","",line)
        line = re.sub("</imagelink.*\n","",line)
        line= re.sub("<group.subwork.image><imagelink>","",line)
        #print line
        #line2 = "<figure>\n<img src=\"" + line + "\" />\n"
        line2 = "<figure>\n<a href=\"" + line + "?buttons=y \"target=\"_blank\"><img src=\"" + line + "\"></a>\n"
        target.write(line2)
        # print line2
    
    elif re.search(".<group.subwork.title>.*",line):
        line = portfolio.next()
        line = re.sub("<work.worktype.*","",line)
        line = re.sub("<work.item.*\n","",line)
        line = re.sub("<group.subwork.*","",line)
        line = re.sub("<text>","",line)
        line = re.sub("</text>","",line)
        if re.search(".*<type>.*",line):
            print line
            done
        #line = re.sub("<work.title>","",line)
        #line = re.sub("</work.title>","",line)
        line2c = "<figcaption>" + line + "</figcaption>\n" + line3 + "</figure>"+ "\n\n"
        #print line2c
        #print line3
        target.write(line2c)    
        
    elif re.search(".<work.title>.*",line):
        line = portfolio.next()
        line = re.sub("<work.worktype.*","",line)
        line = re.sub("<work.item.*\n","",line)
        line = re.sub("<group.subwork.*","",line)
        line = re.sub("<text>","",line)
        line = re.sub("</text>","",line)
        if re.search(".*<type>.*",line):
            print line
            break
        line2c = "<figcaption>" + line + "</figcaption>\n" + line3 + "</figure>"+ "\n\n"
        #print line2c
        #print line3
        target.write(line2c)

line4 = "<hr /></body></html>"
target.write(line4)
target.close()
