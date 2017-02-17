#!/usr/bin/python
import re,sys,os,os.path,subprocess,tempfile,time
from preprocessing import preProcess, cleanTitle
from operator import itemgetter

#input variables/config
#----------------------
inputDir = "../articles"
tempDir = "../temp"
outputDir = "../medavox.github.io"
tagPagesDir = "tags"
tagPageTitlePrefix = "Pages Tagged '"
markdown_flavour = "markdown+pipe_tables+autolink_bare_uris+inline_notes"

#variable initialisation
#-------------------
filesChanged = False
titlesDict = dict()
tagDict = dict()


#function definitions
#--------------------
def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0755)

"""
returns a derived title for the given markdown file.
The title is worked out from its markdown title or, failing that, its file name.
works in both python and bash.
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
	for mo in pat.finditer(contents):
		rawTags = mo.group(1)
		
		#remove any spaces before or after the separating comma; but keep tag-internal spaces
		pat = re.compile(' ?, ?') 
		cleanedCommas = pat.sub( ',', rawTags)
		
		retlist = retlist + cleanedCommas.split(',')
		#print filename+":"+str(retlist)
	return retlist

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
def parseTags(nope):
	notags = []
	#from %tags, create a global one-to-many associative array (dictionary) of tags to pages
	for f in os.listdir(inputDir):
		if f.endswith('.md'):
			tagList = getTags(inputDir+"/"+f)
			#print "tags found:"+str(len(tagList))
			#print f+":"+str(type(tagList))
			if len(tagList) > 0:
				for tag in tagList:
					if tag in tagDict:
						tagDict[tag].append(f)#add this file's name to listvalue of this tagkey
					else: #initialise this tagkey with a new list containing this filename
						tagDict[tag] = [f]
			else:
				print "UNTAGGED: "+f
				notags.append(f)

	allTags = open('../temp/all_tags.md', 'w')
	allTags.write("# All Tags\n\ntag | articles\n----|------\n") #tags as table
	
	untagged = open('../temp/untagged_articles.md', 'w')
	untagged.write("# Untagged Articles\n\n")
	
	for page in notags:
		untagged.write("* ["+getTitle("../articles/"+page)[0]+"]("+cleanTitle(page)[:-2]+"html)\n")
	
	#create a page for every tag found in all the articles.
	#on that page, add a link to every article with that tag
	for tag in tagDict.keys():
		#consider sorting tags before printing
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
			title = getTitle(inputDir+"/"+page)[0]
			tagPage.write("* ["+title+"]("+link+")\n")
			
			#print "\t\""+title+"\" at "+link
		tagPage.close()
	allTags.close()

#actual code execution begins
#----------------------------
for liveFile in os.listdir(inputDir):
	if liveFile.endswith(".md") or liveFile.endswith(".list"):
		thisFileChanged = False
		cleanedName = cleanTitle(liveFile) #replace spaces with underscores in filenames; make the name lowercase as well
		
		exists = os.path.exists("../lastinput/"+cleanedName) #and os.path.isfile("../lastinput/"+cleanedName)
		if exists:
			dift = subprocess.call(["diff", "-q", inputDir+"/"+liveFile, "../lastinput/"+cleanedName])
			if dift != 0:
				filesChanged = True
				thisFileChanged = True
		else: # if there's no copy of this file in ../lastinput, then it has changed by definition
			filesChanged = True
			thisFileChanged = True
		
		if thisFileChanged: # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
			#print ""+liveFile+" HAS CHANGED!"
			guaranteeFolder("../temp")
			
			#print "copying "+liveFile+" to ../temp/"+cleanedName
			subprocess.call(["cp", inputDir+"/"+liveFile, "../temp/"+cleanedName]) # copy changed files to ../temp/ for rendering, in the next loop

			#add derived title to a bash associative array for use by pandoc later
			tytl = getTitle(inputDir+"/"+liveFile)
			titlesDict[cleanedName] = tytl
#fileChanged=True	#debug statement

print "any input file changed:"+str(filesChanged)

#todo: need to regenerate tags into bash dictionary once tagpage mdfiles have been generated
if filesChanged: #if any files have changed, regenerate the tags
	parseTags(None)	#regenerate tag pages

guaranteeFolder(outputDir)
guaranteeFolder(outputDir+"/"+tagPagesDir)
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
	
		padding = "                        "[len(x):]
		print ""+x+":"+padding+"\""+title+"\""
		
		
		with open("../temp/"+x,'r') as fileContents:
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

		args='pandoc -s' #base, and '-s' flag -- creates a standalone doc
		args=args+' -M title="'+title+'"' #title
		args=args+' -c '+stylePathInfix+'style/style.css ' #stylesheet
		args=args+'-c '+stylePathInfix+'style/side-menu.css' #sidemenu style
		args=args+' --template=../rendering/template.html' #use template
		args=args+' -B ../rendering/sidebar.html' #sidebar
		args=args+' -r '+markdown_flavour+' -w html' #in-out formats
		args=args+' -o '+outputDir+'/'+tagPageDir+x[:-2]+'html' #output file

		yum=subprocess.Popen(args, shell=True, stdin=subprocess.PIPE)
		yum.communicate(inputFile)
	
	elif x.endswith(".list"): # TODO
		pass
	
	if isTagPage:#this file is a tag page, don't copy it to lastinput
		subprocess.call(["rm", "../temp/"+x])
	else:#move the file we worked on into lastinput/ for comparison with the copy in articles/ during the next run
		subprocess.call(["mv", "../temp/"+x, "../lastinput/"+x])
	
	#copy the stylesheets into somewhere nginx can reach them
	subprocess.call(["cp", "-R", "../style", outputDir+"/"])
