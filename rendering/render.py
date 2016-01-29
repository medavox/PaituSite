#!/usr/bin/python
import re,sys,os,os.path,subprocess
#shopt -s extglob ##enable better bash regex support, ie for the ?(pattern) below

fileChanged = False
titles = dict()

def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0744)

"""
returns the derived title of a given mdfile, whether from its markdown title, or its file name.
works in both python and bash.
"""
def getTitle(filename):
	openMd = open(filename, 'r')
	#contents = openMd.read()
	contents = openMd.readline() + openMd.readline() #get first two lines as a str; basically head -n 2
	#print contents
	pat = re.compile('^(.+)\n===+$', re.MULTILINE)
	pat2 = re.compile('^# ?(.+)$', re.MULTILINE)
	suche = pat.search(contents)
	if suche == None:
		suche = pat2.search(contents)
	#print suche
	if not suche == None:
		return (suche.group(1), True)
	else: #if the article text contains no discernible title, use the file name
		nopath = filename.split("/")[-1]
		if nopath.endswith(".md"):
			return (nopath[:-3], False)
		else:
			return (nopath, False)

for liveFile in os.listdir("../articles"):
	if liveFile.endswith(".md"):
		cleanedName = liveFile.lower().replace(' ', '_') #replace spaces with underscores in filenames; make the name lowercase as well
		
		#print dift
		exists = os.path.exists("../lastinput/"+cleanedName) #and os.path.isfile("../lastinput/"+cleanedName)
		if exists:
			dift = subprocess.call(["diff", "-q", "-N", liveFile, "../lastinput/"+cleanedName])
			fileChanged = dift != 0
		else: # if there's no copy of this file in ../lastinput, then it has changed by definition
			fileChanged = True
		
		if fileChanged: # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
			#print ""+liveFile+" HAS CHANGED!"

			guaranteeFolder("../temp")
			
			print "copying "+liveFile+" to ../temp/"+cleanedName
			subprocess.call(["cp", "../articles/"+liveFile, "../temp/"+cleanedName]) # copy changed files to ../temp/ for rendering, in the next loop

			#add derived title to a bash associative array for use by pandoc later
			tytle = getTitle("../articles/"+liveFile)
			titles[cleanedName] = tytle


#todo: need to regenerate tags into bash dictionary once tagpage mdfiles have been generated
if fileChanged: #if any files have changed, regenerate the tags
	TagParser	#regenerate tag pages

guaranteeFolder("../html")
guaranteeFolder("../lastinput")
	

for x in os.listdir("../temp"):
	if x.endswith(".md"):
		print "rendering "+x+" to "+x[:-2]+"html"
	
	# extract a title from the doc first line, if the second line is r"===*"
	inDocTitle = titles[x][1]
	title=titles[x][0]
	
	print "title is "+title
	
	fileContentsAsLines = open("../temp/"+x,'r').readlines()

	if inDocTitle: #if there's an in-document title, delete it from appearing in the document body
		inputFile = "".join(fileContentsAsLines[2:])
	else:
		inputFile = "".join(fileContentsAsLines)
#----------------converted to here
	
	#HERE is where we can do the final pre-processing before passing the resulting mdfile to pandoc
	#inputFile="$(../rendering/finalPreprocessor.py "$(echo "$inputFile")" )"
	
	#echo "$inputFile" | pandoc -M title="$title" -B ../rendering/tagEntries.html\
	#	-c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s\
	#	-r markdown+pipe_tables+autolink_bare_uris+inline_notes -w html -o ../html/${x%md}html
	#remember the pandoc --toc argument

	#mv "$x" "../lastinput/$x"
