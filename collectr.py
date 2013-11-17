# The collectr script parse Final Cut Pro XML file searching tag <name> in <clipitem> in <video>. 
# Then it write founded filenames to the OUTPUT text file. After that, script replace ".mov" at 
# the end of filenames with ".RDC" and make search on VOLUME then copy founded RDC folder to the PATH.
# If text file already exist in specified path than script read its content without parsing XML.

#import sys, getopt
import os.path, re, subprocess
import xml.etree.ElementTree as etree
import argparse
from time import sleep

__author__ = 'Robocam'

#Set arguments
parser = argparse.ArgumentParser(description='Final Cut Pro XML source collector')
parser.add_argument('-i','--input', help='Input XML file name', required=True)
parser.add_argument('-o','--output', help='Output TXT file name', required=False)
parser.add_argument('-v','--volume', help='Volume name where to search R3D files', required=False)
parser.add_argument('-p','--path', help='Path where to copy R3D files', required=False)
args = parser.parse_args()

#Set input XML filename from args
xmlName = args.input

# Set text filename from args or by default
if args.output:
	txtName = args.output
else: 
	txtName = args.input + '.txt'

# Set Volume from args or by default
if args.volume:
	volName = '/Volumes/' + args.volume
else:
	volName = '/Volumes'
print '\n' + 'R3D files will search in ' + volName + '...'

# Set path to copy R3D files
if args.path:
	pathName = args.path + '/'
else:
	pathName = '$PWD'
print 'R3D files will be copied to ' + pathName

#Make text file with all R3D filenames from XML
fileCount = 0
if not os.path.exists(txtName):
	txtfile = open(txtName, 'w+')
	tree = etree.parse(xmlName)
	root = tree.getroot()
	for elem in root.findall(".//sequence/media/video/track/clipitem/file/name"):
		match = re.match("^[A-Z]\d{3}_[A-Z]\d{3}_\d{4}\w{2}.mov", elem.text)
		if match:
			txtfile.write(elem.text + '\n')
			fileCount += 1
	print 'Found ' + str(fileCount) + ' file(s)'
	txtfile.close
else:
	print 'Text file already exists, reading contents...'

sleep(3)

#Open text file and read content
txtfile = open(txtName, 'r')
pathurls = txtfile.readlines()
fileCount = len(pathurls)
txtfile.close

lineCount = 1
R3Dname = ''

#Find and copy R3D files
txtfile = open(txtName, 'w+')
for filename in pathurls:
	R3Dname = filename[0:16] + '.RDC'
	#result = subprocess.check_output(['find', volName, '-type', 'd', '-name', R3Dname, '-exec', 'cp', '-R', '{}', pathName, ';']) 
	finded = subprocess.check_output(['find', volName, '-type', 'd', '-name', R3Dname]) 
	if finded:
		print filename.rstrip('\n') + ' --------------- ' + str(lineCount) + ' of ' + str(fileCount)
		subprocess.call(['cp', '-R', finded.rstrip(), pathName])
		print finded
		lineCount += 1
	else:
		txtfile.write(filename)

print 'Found and copied ' + str(lineCount-1) + ' file(s) of ' + str(fileCount)

