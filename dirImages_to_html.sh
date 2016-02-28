#!/bin/bash

#
# Run from within a directory of JPG images to produce a webpage with all of the images embedded.
#

# generate list of JPG files in current directory
ls -1 *.jpg  > filelist.txt

# If imageIndex.html exists, rename it so we can build a new one
if [ -e ./imageIndex.html ]
then
mv imageIndex.html "index_"$SECONDS".html"
fi

# remove any existing imageIndex.html file
# rm imageIndex.html

echo "<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>BIll Rules!</title>
</head>
</body>
" >> imageIndex.html

# TEST #while read line; do echo "$line"; done < filelist.txt

while read line; do echo "<a href=\"./$line.html\"><img src=\"$line\" alt=\"[$line]\" width=\"800\" /></a></br></br>
" >> imageIndex.html; done < filelist.txt

echo "</body><hr /></html>" >> imageIndex.html

## Build individual web pages for individual images

while read line; do echo "
<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>$line</title></head>
<body><img src=\"$line\" /><hr/><a href=\"imageIndex.html\">Back</a></body></html>" > $line.html;done < filelist.txt
