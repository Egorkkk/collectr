collectr
========

Collect R3D files by Final Cut Pro XML

-i INPUT 
		path to XML file.

-o OUTPUT 
		path to TXT file with R3D names. Optional. 
		By default file will be created in script folder with name of input XML.

-v VOLUME 
		volume name where to search R3D files Optional. By default searching in /Volumes folder.

-p PATH 
		path to copy RDC folders. Optional. By default RDC folders will be copied to current folder. 
		Path must be exists if argument specified.


The collectr script parse Final Cut Pro XML file searching tag <name> in <clipitem> in <video>. 
Then it write founded filenames to the OUTPUT text file. After that, script replace ".mov" at 
the end of filenames with ".RDC" and make search on VOLUME then copy founded RDC folder to the PATH.
If text file already exist in specified path than script read its content without parsing XML.


