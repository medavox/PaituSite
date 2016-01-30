#!/usr/bin/python
import re,sys,os,os.path,subprocess,tempfile,time
from preprocessing import preProcess, cleanTitle
from operator import itemgetter

docsDir = "../articles"

filesChanged = False
titlesDict = dict()
tagDict = dict()

tagPageTitlePrefix = "Pages Tagged '"

def guaranteeFolder(folderName):
	if not os.path.isdir(folderName):
		os.mkdir(folderName, 0755)



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
		rawTags = mo.group(1)
		pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
		cleanedCommas = pat.sub( ',', rawTags)
		retlist = retlist + cleanedCommas.split(',')
		#print filename+":"+str(retlist)
	return retlist

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
def parseTags(nope):
	notags = []
	#from %tags, create a global one-to-many associative array (dictionary) of tags to pages
	for f in os.listdir(docsDir):
		if f.endswith('.md'):
			tagList = getTags(docsDir+"/"+f)
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
		
		allTags.write("["+tag+"]("+cleanTitle(tag)+".html) | "+str(len(tagDict[tag]))+"\n")#tags as table
		
		tagPage = open('../temp/'+cleanTitle(tag)+'.md', 'w')
		tagPage.write(tagPageTitlePrefix+tag+"'\n===\n\n") # write page title
		padding = "                "[len(tag):]
		print tag+":"+padding+str(len(tagDict[tag]))+" articles"
		for page in tagDict[tag]:
			link = cleanTitle(page)[:-3]+".html"
			title = getTitle(docsDir+"/"+page)[0]
			tagPage.write("* ["+title+"]("+link+")\n")
			
			#print "\t\""+title+"\" at "+link
		tagPage.close()
	allTags.close()

#--------------------begin!
for liveFile in os.listdir(docsDir):
	if liveFile.endswith(".md") or liveFile.endswith(".list"):
		thisFileChanged = False
		cleanedName = cleanTitle(liveFile) #replace spaces with underscores in filenames; make the name lowercase as well
		
		exists = os.path.exists("../lastinput/"+cleanedName) #and os.path.isfile("../lastinput/"+cleanedName)
		if exists:
			dift = subprocess.call(["diff", "-q", docsDir+"/"+liveFile, "../lastinput/"+cleanedName])
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
			subprocess.call(["cp", docsDir+"/"+liveFile, "../temp/"+cleanedName]) # copy changed files to ../temp/ for rendering, in the next loop

			#add derived title to a bash associative array for use by pandoc later
			tytl = getTitle(docsDir+"/"+liveFile)
			titlesDict[cleanedName] = tytl
#fileChanged=True	#debug statement

print "fileschanged:"+str(filesChanged)

#todo: need to regenerate tags into bash dictionary once tagpage mdfiles have been generated
if filesChanged: #if any files have changed, regenerate the tags
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
	
		padding = "                        "[len(x):]
		print ""+x+":"+padding+"\""+title+"\""
		
		with open("../temp/"+x,'r') as fileContents:
			asLines = fileContents.readlines()
		
		if inDocTitle: #if there's an in-document title, delete it from appearing in the document body
			inputFile = "".join(asLines[2:])
		else:
			inputFile = "".join(asLines)
		
		#HERE is where we do the final pre-processing before passing the resulting mdfile to pandoc		
		inputFile = preProcess(inputFile)

		args='pandoc -M title="'+title+'" -c style/style.css -c style/side-menu.css --template=../rendering/template.html -B ../rendering/sidebar.html -s -r markdown+pipe_tables+autolink_bare_uris+inline_notes -w html -o ../html/'+x[:-2]+'html'
		#print args
		yum=subprocess.Popen(args, shell=True, stdin=subprocess.PIPE)
		yum.communicate(inputFile)
	
	elif x.endswith(".list"): # TODO
		pass
	
	if asLines[0].startswith(tagPageTitlePrefix):#this file is a tag page, don't copy it to lastinput
		#print x+" is a tag page"
		subprocess.call(["rm", "../temp/"+x])
	else:#move the file we worked on into lastinput/ for comparison with the copy in articles/ during the next run
		#print x+" is NOT a tag page"
		subprocess.call(["mv", "../temp/"+x, "../lastinput/"+x])
	
	#copy the stylesheets into somewhere nginx can reach them
	subprocess.call(["cp", "-R", "../style", "../html/"])
