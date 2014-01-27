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
parser = argparse.ArgumentParser(description='Final Cut Pro XML and Davinci Resolve source collector')
parser.add_argument('-i','--input', help='Input XML file name', required=True)
parser.add_argument('-t','--type', help='[F]inal Cut Pro or [D]avinci Resolve', required=True)
parser.add_argument('-s','--source', help='[A]rri Alexa or [R]3D source files', required=True)
parser.add_argument('-o','--output', help='Output TXT file name', required=False)
parser.add_argument('-v','--volume', help='Volume name where to search R3D files', required=False)
parser.add_argument('-p','--path', help='Path where to copy R3D files', required=False)
parser.add_argument('-l','--list', help='[Y] - Makes only txt file with source filenames without find and copy', required=False)
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

#Select XML schema query
if args.type == 'F':
	xmlPath = ".//sequence/media/video/track/clipitem/file/name"
else:
	#xmlPath = ".//SM_Project/TimeLineVec/Element/Sm2Timeline/Sequence/Sm2Sequence/VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/Name"
	#xmlPath = ".//SM_Project/TimeLineVec/Element/Sm2Timeline/Sequence/Sm2Sequence/VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/MediaReelNumber"
	xmlPath = ".//VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/MediaReelNumber"

#Regexp for search in XML
if args.source == 'R':
	xmlSearch = "^[A-Z]\d{3}_[A-Z]\d{3}_\d{4}\w{2}" # For R3D
else:
	xmlSearch = "^[A-Z]\d{3}[A-Z]\d{3}_\d{4}\w{2}" # For Alexa

#Make text file with all R3D filenames from XML
fileCount = 0
if not os.path.exists(txtName):
	txtfile = open(txtName, 'w+')
	tree = etree.parse(xmlName)
	root = tree.getroot()
	# for elem in root.findall(".//sequence/media/video/track/clipitem/file/name"):
	# for elem in root.findall(".//VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/Name"):
	for elem in root.findall(".//VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/MediaReelNumber"):
		# match = re.match("^[A-Z]\d{3}_[A-Z]\d{3}_\d{4}\w{2}.mov", elem.text) # PROXY
		# match = re.match("^[A-Z]\d{3}_[A-Z]\d{3}_\d{4}\w{2}", elem.text) # RED
		# match = re.match("^[A-Z]\d{3}[A-Z]\d{3}_\d{4}\w{2}", elem.text) # Alexa
		match = re.match(xmlSearch, elem.text) 
		if match:
			txtfile.write(elem.text + '\n')
			fileCount += 1
	print 'Found ' + str(fileCount) + ' cut(s)'
	txtfile.close
	txtfile = open(txtName, 'r')
	tempurls = txtfile.readlines()
	pathurls = list(set(tempurls))
	fileCount = len(pathurls)
	txtfile.close
	print 'Found ' + str(fileCount) + ' file(s)'
else:
	print 'Text file already exists, reading contents...'

if args.list != 'Y':
	sleep(3)

	#Open text file and read content

	txtfile = open(txtName, 'r')
	tempurls = txtfile.readlines()
	pathurls = list(set(tempurls))
	fileCount = len(pathurls)
	txtfile.close

	lineCount = 1
	R3Dname = ''

	#Find and copy R3D files
	txtfile = open(txtName, 'w+')
	for filename in pathurls:
		if args.source == 'R':
			R3Dname = filename[0:16] + '.RDC' # RED
			finded = subprocess.check_output(['find', volName, '-type', 'd', '-name', R3Dname]) # RED
		else:
			R3Dname = filename[0:20] + '*' + '.mov' # Alexa
			finded = subprocess.check_output(['find', volName, '-type', 'f', '-name', R3Dname]) 

		if finded:
			print filename.rstrip('\n') + ' --------------- ' + str(lineCount) + ' of ' + str(fileCount)
			subprocess.call(['cp', '-R', finded.rstrip(), pathName])
			print finded
			lineCount += 1
		else:
			txtfile.write(filename)
			
else if args.list = 'Y':
	return 0

print 'Found and copied ' + str(lineCount-1) + ' file(s) of ' + str(fileCount)

