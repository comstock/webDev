#!/usr/bin/python
#import os, sys
import re

# BUG: Apparently some items have more than one work.title, and in these cases the image/image-caption pairs fall out of sync, and images become mis-captioned on the output html page.

from xml.dom import minidom
XML = '/home/comstock/Downloads/Transformed_records.xml'
CNT = 1
target = open("via.html", 'w')

doc = minidom.parse(XML)

element = doc.getElementsByTagName("imagelink")
count = len(element)
#print count

line1 = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n\
<head>\n\
   <title>Images from VIA </title>\n\
		<link rel=\"stylesheet\" href=\"http://www.w3.org/StyleSheets/Core/Traditional\" type=\"text/css\" />\n\
   </head>\n\
   <body>\n"
target.write(line1)

while CNT < count:
    ##print(name.firstChild.data)
    
    jelly = doc.getElementsByTagName("imagelink")[CNT]
    jammy = doc.getElementsByTagName('work.title')[CNT]
    # print jammy.toxml()
    #print "<img src=\"" + (jelly.firstChild.data) + "\" />"
    line2 = "<figure>\n<img src=\"" + (jelly.firstChild.data) + "\" />\n"
    line2c = "<figcaption>" + (jammy.toxml()) + "</figcaption>\n</figure>" + "<br />\n\n"
    line2c = re.sub("<text>","",line2c)
    line2c = re.sub("</text>","",line2c)
    line2c = re.sub("<work.title>","",line2c)
    line2c = re.sub("</work.title>","",line2c)
    target.write(line2)
    target.write(line2c)
    #link = doc.getElementsByTagName("imagelink")[CNT]
    #print link
    CNT = CNT + 1
line3 = "</body></html>"
target.write(line3)
target.close()
'''
target = open("via.html", 'r+')
for line in target:
    #target.write(re.sub("<text>","ZZZZZZZZZZZZ", line))
    zeb = line
    #zeb = re.sub("<text>","", zeb)
    #target.write(zeb)
    #zeb = re.sub("<\/text>","", zeb)
    #zeb = re.sub("<text>(.*)</text>","\1",zeb)
    zeb = re.sub("<work.title>","", zeb)
    zeb = re.sub("<\/work\.title>","",zeb)
    zeb = re.sub("<type>.*","",zeb)
    
    print zeb
    target.write(zeb)
    '''
