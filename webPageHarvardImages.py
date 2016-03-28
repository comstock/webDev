#!/usr/bin/python
#import os, sys
import re
from xml.dom import minidom
XML = '/home/comstock/Documents/20160323_Transformed_records.xml'
libCloud_stem = 'http://api.lib.harvard.edu/v2/items?url='
CNT = 1
target = open("list-of-urns.txt", 'w')

doc = minidom.parse(XML)

link = doc.getElementsByTagName("imagelink")
count = len(link)
print count

rec_id = doc.getElementsByTagName("via_id")
rec_count = len(rec_id)
print "RECORDS = " + str(rec_count)

while CNT != count:
    record = doc.getElementsByTagName("imagelink")[CNT]
    line = record.toxml()
    line = re.sub("<imagelink>","",line)
    line = re.sub("</imagelink>","",line)
    print line
    target.write(line + "\n")
    CNT = CNT + 1
    
target.close()
