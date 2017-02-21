#!/usr/bin/python
import re,sys,os,os.path,subprocess,tempfile,time,datetime
from preprocessing import preProcess, cleanTitle
from operator import itemgetter

#input variables/config
#----------------------
inputDir = "../articles/"
tempDir = "../temp/"
lastInput="../lastinput/"
outputDir = "../medavox.github.io/"
tagPagesDir = "tags"
tagPageTitlePrefix = "Pages Tagged '"
markdown_flavour = "markdown+pipe_tables+autolink_bare_uris+inline_notes"

#variable initialisation
#-------------------
filesChanged = False
titlesDict = dict()
tagDict = dict()
notags = []

#function definitions
#--------------------
def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0755)

"""
returns a derived title for the given markdown file.
The title is worked out from its markdown title or, failing that, its file name.
works in both python and bash.;l
"""
def getTitle(filename):
	openMd = open(filename, 'r')
	#todo:guard against blank leading lines
	contents = openMd.readline() + openMd.readline() #get first two lines as a str; basically head -n 2

	pat = re.compile('^(.+)\n===+$', re.MULTILINE)
	suche = pat.search(contents) #try using the line above '===', if it exists
	if suche == None: # if that fails, try using the line beginning with '#'
		pat2 = re.compile('^# ?(.+)$', re.MULTILINE)
		suche = pat2.search(contents)

	if suche == None:#if that fails, return the filename
		nopath = filename.split("/")[-1]
		#todo: generalise to removing any file extension
		if nopath.endswith(".md"):#strip .md extension if it exists
			return (nopath[:-3], False)
		else:
			return (nopath, False)
	else: #if suche wasn't null, return the result of the regex search
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
	for mo in pat.finditer(contents):#match obj;
		#we're only expecting 1 match per file, but just in case
		rawTags = mo.group(1)

		#remove any spaces before or after the separating comma; but keep tag-internal spaces
		pat = re.compile(' ?, ?')
		cleanedCommas = pat.sub( ',', rawTags)

		retlist = retlist + cleanedCommas.split(',')
		#print filename+":"+str(retlist)
	return retlist

def addTagsToDict(f):
	tagList = getTags(inputDir+f)
	#print "tags found:"+str(len(tagList))
	#print f+":"+str(type(tagList))
	if len(tagList) > 0:
		for tag in tagList:
			if tag in tagDict:
				tagDict[tag].append(f)#add this file's name to listvalue of this tagkey
			else: #initialise this tagkey with a new list containing this filename
				tagDict[tag] = [f]
	else:#if there are no tags detected in the file, add it to a list
		print "UNTAGGED: "+f
		notags.append(f)

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
#from %tag lines in files, create a global map of [tags]:1 to [files with that tag]:n

def convertTagDictToTagPages():
	allTags = open(tempDir+'all_tags.md', 'w')
	allTags.write("# All Tags\n\ntag | articles\n----|------\n") #tags as table

	#create page of untagged articles
	untagged = open(tempDir+'untagged_articles.md', 'w')
	untagged.write("# Untagged Articles\n\n")

	for page in notags:
		untagged.write("* ["+getTitle("../articles/"+page)[0]+"]("+cleanTitle(page)[:-2]+"html)\n")
	untagged.close()

	#create a page for every tag found in all the articles.
	#on that page, add a link to every article with that tag
	for tag in tagDict.keys():
		#todo: sort tags alphabetically before printing
		#sorted(tagDict, key=itemgetter(len(tagDict[tag])), reverse=True)
		#articlesPerTag.append((tag, len(tagDict[tag])))
		#allTags.write("* ["+tag+"]("+cleanTitle(tag)+".html): "+str(len(tagDict[tag]))+" articles\n")#as bulleted list

		allTags.write("["+tag+"](tags/"+cleanTitle(tag)+".html) | "+str(len(tagDict[tag]))+"\n")#tags as table

		tagPage = open(tempDir+'/'+cleanTitle(tag)+'.md', 'w')
		tagPage.write(tagPageTitlePrefix+tag+"'\n===\n\n") # write page title
		padding = "                "[len(tag):]
		print tag+":"+padding+str(len(tagDict[tag]))+" articles"
		for page in tagDict[tag]:
			link = "../"+cleanTitle(page)[:-3]+".html"
			title = getTitle(inputDir+page)[0]
			tagPage.write("* ["+title+"]("+link+")\n")
			#print "\t\""+title+"\" at "+link
		tagPage.close()
	allTags.close()

def addModifiedTime(filePath, fileContents):
	modTime = os.path.getmtime(filePath)
	niceDate = datetime.datetime.fromtimestamp(modTime).strftime('%Y-%m-%d %H:%M:%S')
	return fileContents + "\n\n (last modified on "+niceDate+")"

#actual code execution begins
#----------------------------
for liveFile in os.listdir(inputDir):
	if liveFile.endswith(".md") or liveFile.endswith(".list"):
		thisFileChanged = False
		cleanedName = cleanTitle(liveFile) #replace spaces with underscores in filenames; make the name lowercase as well

		if os.path.exists(lastInput+cleanedName):
			dift = subprocess.call(["diff", "-q", inputDir+liveFile, lastInput+cleanedName])
			if dift != 0:
				filesChanged = True
				thisFileChanged = True
		else: # if there's no copy of this file in ../lastinput, then it has changed by definition
			filesChanged = True
			thisFileChanged = True

		if thisFileChanged: # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
			guaranteeFolder(tempDir)
			# copy changed files to ../temp/ for rendering, in the next loop
			subprocess.call(["cp", inputDir+liveFile, tempDir+cleanedName])

			#only regenerate tags from pages that have changed
			addTagsToDict(liveFile)

			#add derived title to a bash associative array for use by pandoc later
			tytl = getTitle(inputDir+liveFile)
			titlesDict[cleanedName] = tytl
#fileChanged=True	#debug statement

print "any input file changed:"+str(filesChanged)

if filesChanged: #if any files have changed, regenerate the tags
	convertTagDictToTagPages()

guaranteeFolder(outputDir)
guaranteeFolder(outputDir+tagPagesDir)
guaranteeFolder(lastInput)

for x in os.listdir(tempDir):
	if x.endswith(".md"):
		if x in titlesDict:
			inDocTitle = titlesDict[x][1]
			title = titlesDict[x][0]
		else:
			titleTuple = getTitle(tempDir+x)
			title = titleTuple[0]
			inDocTitle = titleTuple[1]

		padding = "                        "[len(x):]
		print ""+x+":"+padding+"\""+title+"\""

		with open(tempDir+x,'r') as fileContents:
			asLines = fileContents.readlines()

		tagPageDir		= ""
		stylePathInfix	= ""
		isTagPage = asLines[0].startswith(tagPageTitlePrefix)
		#change the path to the stylesheets and tag pages, if this is a tag page
		if isTagPage:
			tagPageDir = tagPagesDir+"/"
			stylePathInfix = "../"

		if inDocTitle: #if there's an in-document title, delete it from appearing in the document body
			inputFile = "".join(asLines[2:])
		else:
			inputFile = "".join(asLines)

		#do final pre-processing (see preprocessing.py) before passing the resulting mdfile to pandoc
		inputFile = preProcess(inputFile)

		#check for %contents or %toc tag, instructing us to add a table of contents
		tocPattern = re.compile(r"^%(contents|toc)", re.MULTILINE)
		tableOfContents = False
		if re.search(tocPattern, inputFile) != None:
			#file contains at least one instance of %toc or %contents
			tableOfContents = True
			inputFile = re.sub(tocPattern, "", inputFile)#remove the tag

		#add last modification time to article
		inputFile = addModifiedTime(tempDir+x, inputFile)

		#-----------------------------------------------------------------------
		#document pre-processing over, time to send the results to pandoc

		args='pandoc -s' #base, and '-s' flag -- creates a standalone doc
		args=args+' -M title="'+title+'"' #title
		args=args+' -c '+stylePathInfix+'style/style.css' #stylesheet
		args=args+' -c '+stylePathInfix+'style/side-menu.css' #sidemenu style
		args=args+' --template=../rendering/template.html' #use template
		args=args+' -B ../rendering/sidebar.html' #sidebar
		if tableOfContents:
			args=args+' --table-of-contents'#optional table of contents
		args=args+' -r '+markdown_flavour+' -w html' #in-out formats
		args=args+' -o '+outputDir+'/'+tagPageDir+x[:-2]+'html' #output file

		yum=subprocess.Popen(args, shell=True, stdin=subprocess.PIPE)
		yum.communicate(inputFile)

	elif x.endswith(".list"): # TODO
		pass

	if isTagPage:#this file is a tag page, don't copy it to lastinput
		subprocess.call(["rm", tempDir+x])
	else:#move the file we worked on into lastinput/ for comparison with the copy in articles/ during the next run
		subprocess.call(["mv", tempDir+x, lastInput+x])

	#copy the stylesheets into somewhere nginx can reach them
	subprocess.call(["cp", "-R", "../style", outputDir])
