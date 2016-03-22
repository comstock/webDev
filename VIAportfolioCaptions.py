#!/usr/bin/python
#import os, sys
import re
from xml.dom import minidom

XML = '/home/comstock/Documents/Transformed_records_trim.xml'
CNT = 1
target = open("sailing.html", 'w')
portfolio = open(XML, 'r')
doc = minidom.parse(XML)
element = doc.getElementsByTagName("imagelink")
count = len(element)
print "IMAGELINK COUNT = " + str(count)


title = doc.getElementsByTagName('work.title')

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
    if re.search(".*imagelink.*", line):
        line = re.sub("<work.image><imagelink>","",line)
        line = re.sub("</imagelink.*\n","",line)
        line= re.sub("<group.subwork.image><imagelink>","",line)
        #print line
        line2 = "<figure>\n<img src=\"" + line + "\" />\n"
        target.write(line2)
        print line2
    elif re.search(".*work.title>.*",line):
        line = portfolio.next()
        line = re.sub("<work.worktype.*","",line)
        line = re.sub("<work.item.*\n","",line)
        line = re.sub("<group.subwork.*","",line)
        line2c = "<figcaption>" + line + "</figcaption>\n</figure>"+ "\n\n"
        # print line2c
        target.write(line2c)
        #next()
        
        line = re.sub("<text>","",line)
        line = re.sub("</text>","",line)
        # print line

line3 = "</body></html>"
target.write(line3)
target.close()
