#!/usr/bin/python
#import os, sys
import re
import pycurl
import cStringIO
#from xml.dom import minidom

buf = cStringIO.StringIO()
infile = "/home/comstock/Documents/python/input/via_ids.txt"

target = open("image_specs.html", 'w')
id_list = open(infile, 'r')
iiif_record_syntax_stem = "http://iiif.lib.harvard.edu/manifests/via:"
iiif_image_id_stem = "http://ids.lib.harvard.edu/ids/iiif/"
iif_image_id_tail = "/info.json"

for line in id_list:
    rec_id = line
    rec_manifest = iiif_record_syntax_stem + rec_id
    rec_manifest = rec_manifest.rstrip()    
    print rec_manifest
    
    c = pycurl.Curl()
    c.setopt(c.URL, rec_manifest)
    c.setopt(c.WRITEFUNCTION, buf.write)

    c.perform()
    print buf.getvalue()
    #buf.close()
   
    
    
    
    #img_id = iiif_image_id_stem + 
