#!/usr/bin/python
import re,sys,os,os.path,subprocess,tempfile,time
from preprocessing import preProcess

docsDir = "../articles"

fileChanged = False
titlesDict = dict()
tagDict = dict()

def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0755)

def cleanTitle(title):
	extension = title[title.rfind("."):]
	workingTitle = title[:title.rfind(".")].lower().replace(' ', '_') #har har har
	output = re.sub(r"[^a-z0-9 -]", "", workingTitle)
	
	return output+extension

"""
returns the derived title of a given mdfile, whether from its markdown title, or its file name.
works in both python and bash.
"""
def getTitle(filename):
	openMd = open(filename, 'r')
	contents = openMd.readline() + openMd.readline() #get first two lines as a str; basically head -n 2
	#print contents
	pat = re.compile('^(.+)\n===+$', re.MULTILINE)
	suche = pat.search(contents)
	if suche == None: # if it's not the normal-style header, try the hash one
		pat2 = re.compile('^# ?(.+)$', re.MULTILINE)
		suche = pat2.search(contents)

	if suche == None:
		nopath = filename.split("/")[-1]
		if nopath.endswith(".md"):
			return (nopath[:-3], False)
		else:
			return (nopath, False)
	else: #if the article text contains no discernible title, use the file name
		return (suche.group(1), True)

"""
Creates a page for each tag, with links to each article with that tag.
Tags are found by checking all articles
"""
def getTags(filename):
	openfile = open(filename, 'r')
	contents = openfile.read()
	openfile.close()
	pat = re.compile(r"^%tags?: ?([^\n,]+(,[^\n,]+)*) *$", re.M)
	retlist = []
	for mo in pat.finditer(contents):
	#for mo in pat.sub(contents, re.M):
		rawTags = mo.group(1)
		pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
		cleanedCommas = pat.sub( ',', rawTags)
		retlist = retlist + cleanedCommas.split(',')
		#print filename+":"+str(retlist)
	return retlist

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
def parseTags(nope):
	#from %tags, create a global one-to-many associative array (dictionary) of tags to pages
	for f in os.listdir(docsDir):
		if f.endswith('.md'):
			tagList = getTags(docsDir+"/"+f)
			#print "tags found:"+str(len(tagList))
			#print f+":"+str(type(tagList))
			if type(tagList) is list:
				for tag in tagList:
					if tag in tagDict:
						tagDict[tag].append(f)#add this file's name to listvalue of this tagkey
					else: #initialise this tagkey with a new list containing this filename
						tagDict[tag] = [f]
	#tagEntries = open('../temp/all_tags.html', 'w')
	#tagEntries.write("# All Tags\n")
	
	#create a page for every tag found in all the articles.
	#on that page, add a link to every article with that tag
	for tag in tagDict.keys():
		#consider sorting tags before printing
	#	linkUrl = ""+tag
	#	tagEntries.write("* "+tag+"\n")
	#	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
	#		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
		tagPage = open('../temp/'+cleanTitle(tag)+'.md', 'w')
		#tagPage.write("Pages Tagged '"+tag+"'\n===\n\n") # write page title
		print tag+":"
		for page in tagDict[tag]:
			link = cleanTitle(page)[:-3]+".html"
			title = getTitle(docsDir+"/"+page)[0]
			tagPage.write("* ["+title+"]("+link+")\n")
			
			print "\t\""+title+"\" at "+link
		tagPage.close()
	#tagEntries.close()

#--------------------begin!

for liveFile in os.listdir(docsDir):
	if liveFile.endswith(".md"):
		cleanedName = cleanTitle(liveFile) #replace spaces with underscores in filenames; make the name lowercase as well
		
		exists = os.path.exists("../lastinput/"+cleanedName) #and os.path.isfile("../lastinput/"+cleanedName)
		if exists:
			dift = subprocess.call(["diff", "-q", "-N", liveFile, "../lastinput/"+cleanedName])
			fileChanged = dift != 0
		else: # if there's no copy of this file in ../lastinput, then it has changed by definition
			fileChanged = True
		
		if fileChanged: # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
			#print ""+liveFile+" HAS CHANGED!"

			guaranteeFolder("../temp")
			
			#print "copying "+liveFile+" to ../temp/"+cleanedName
			subprocess.call(["cp", docsDir+"/"+liveFile, "../temp/"+cleanedName]) # copy changed files to ../temp/ for rendering, in the next loop

			#add derived title to a bash associative array for use by pandoc later
			tytl = getTitle(docsDir+"/"+liveFile)
			titlesDict[cleanedName] = tytl

print "filechanged:"+str(fileChanged)

#todo: need to regenerate tags into bash dictionary once tagpage mdfiles have been generated
if fileChanged: #if any files have changed, regenerate the tags
	parseTags(None)	#regenerate tag pages

guaranteeFolder("../html")
guaranteeFolder("../lastinput")
	

for x in os.listdir("../temp"):
	if x.endswith(".md"):
		if x in titlesDict:
			inDocTitle = titlesDict[x][1]
			title = titlesDict[x][0]
		else:
			titleTuple = getTitle("../temp/"+x)
			title = titleTuple[0]
			inDocTitle = titleTuple[1]
		#print "rendering "+x+" to "+x[:-2]+"html"
		#print "titlesDict entry:"+str(titlesDict[x])
	
		print "title is "+title
		
		with open("../temp/"+x,'r') as fileContents:
			asLines = fileContents.readlines()
		
		if inDocTitle: #if there's an in-document title, delete it from appearing in the document body
			inputFile = "".join(asLines[2:])
		else:
			inputFile = "".join(asLines)
		
		#HERE is where we do the final pre-processing before passing the resulting mdfile to pandoc		
		inputFile = preProcess(inputFile)
		
		print "inputFile length:"+str(len(inputFile))

		args='pandoc -M title="'+title+'" -c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s -r markdown+pipe_tables+autolink_bare_uris+inline_notes -w html -o ../html/'+x[:-2]+'html'
		#print args
		yum=subprocess.Popen(args, shell=True, stdin=subprocess.PIPE)
		yum.communicate(inputFile)
	

	#mv "$x" "../lastinput/$x"
