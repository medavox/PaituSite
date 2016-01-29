#!/usr/bin/python
import re,sys,os,os.path,subprocess
from tweaks import preProcess
from TagParser import parseTags
#shopt -s extglob ##enable better bash regex support, ie for the ?(pattern) below

fileChanged = False
titles = dict()

def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0744)

"""
Creates a page for each tag, with links to each article with that tag.
Tags are found by checking all articles
"""
tagDict = dict()

def getTags(filename):
	openfile = open(filename, 'r')
	contents = openfile.read()
	pat = re.compile(r"^%tags?: ?([^,]+(,[^,]+)*)$")
	retlist = []
	for mo in pat.finditer(contents, re.M):
		rawTags = mo.group(1)
		pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
		cleanedCommas = pat.sub( ',', rawTags)
		retlist = retlist + cleanedCommas.split(',')
	return retlist

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

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
def parseTags(nope):
	#parse %tags, creating a global one-to-many associative array (dictionary) of tags to pages
	for f in os.listdir("../articles"):
		if f[-3:] == '.md':
			tagList = getTags("../articles/"+f)
			#print f+":"+str(type(tagList))
			if type(tagList) is list:
				for tag in tagList:
					if tag in tagDict:
						#add this file's name to listvalue of this tagkey
						tagDict[tag].append(f)
					else: #initialise this tagkey with a new list containing this filename
						tagDict[tag] = [f]
	
	#tagEntries = open('../temp/all_tags.html', 'w')
	#tagEntries.write("# All Tags\n")
	
	#create a page for every found tag.
	#on that page, add a link to every article with that tag
	for tag in tagDict.keys():
		#consider sorting tags before printing
	#	linkUrl = ""+tag
	#	tagEntries.write("* "+tag+"\n")
	#	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
	#		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
		tagPage = open('../temp/'+tag.replace(' ', '_').lower()+'.md', 'w')
		#tagPage.write("Pages Tagged '"+tag+"'\n===\n\n") # write page title
		for page in tagDict[tag]:
			link = page.lower().replace(' ', '_')[:-3]+".html"
			title = getTitle("../articles/"+page)
			tagPage.write("* ["+title+"]("+link+")\n")
			print tag+":"
			print "\t\""+title+"\" at "+link
		tagPage.close()
	#tagEntries.close()

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
	parseTags(None)	#regenerate tag pages

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
