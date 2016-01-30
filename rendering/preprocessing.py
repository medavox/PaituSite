#!/usr/bin/python
import re, sys

"""
handles any remaining in-place article substitutions, before sending to pandoc.

such as:

* the %include command,
* making internal links work
* converting the %tag command into a valid markdown list of links to tagpages
"""

#handle includes regexplanation:
# at the beginning of a line: 0 or more of: (1 or more non-slashes followed by a slash),
# followed by 0 or more nonslashes (the filename),
# followed by a dot, then 1-10 ascii latin characters (the file extension). End of line.
# extensionless files are not supported, because they usually don't show up on the internet,
# and if they did, they would seem suspicious anyway

tagDict = dict()

"""
this needs to be here (instead of in render.py, where it is used more),
because preprocessor.py can't import functions from render.py;
i think something about python prohibiting imports happening both ways between files
"""
def cleanTitle(title):
	extension = title[title.rfind("."):]
	workingTitle = title[:title.rfind(".")].lower().replace(' ', '_') #har har har
	output = re.sub(r"[^a-z0-9 _-]", "", workingTitle)
	return output+extension


def includer(matchObj):
	#print "includer"
	includingFileName = matchObj.group(1)
	#print "found file name:"+includingFileName
	openedFile = open("../articles/"+includingFileName, 'r')
	return openedFile.read()

"""
replaces the %tag(s): Paitu command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
the actual regex function for creating lists of tags, which generates the markdown
"""
def tagLister(matchObj):
	#print "taglister"
	rawTags = matchObj.group(1)
	pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
	cleanedCommas = pat.sub( ',', rawTags)
	
	#tagfoot = "<p>Tagged as: " # html-output version
	tagfoot = "\n\nTagged as: " # markdown-output
	for tag in cleanedCommas.split(','):
		tagfoot += "["+tag+"]("+cleanTitle(tag) + ".html) " # markdown
	return tagfoot+"\n"

def internalLinker(matchObj):
	#print matchObj.group(1) #[case-insensitive internal link](
	#print matchObj.group(2) #<the path before the filename in the link 'url'>
	#print matchObj.group(3) #chat bOt project
	out = matchObj.group(1)
	linkName = matchObj.group(2).lower().replace(' ', '_')
	return out +linkName+".html)"#+"LINKA!GROVE!"
	

conversionRules = \
[(r"^%tags?: ?([^\n,]+(,[^\n,]+)*) *$", 				tagLister),			#handle tag list
 (r"(\[[^\]\n]+\]\()([\w _-]+)\)", 						internalLinker), 	#handle internal links
 (r"^<a:([\w-]+)>",										r'<a name="\1"></a>'),#expand shortened anchor syntax to full html # TODO
 (r"^%include (([^/]+/)*/?[^/]*\.[a-zA-Z0-9]{1,10})$",	includer)]			#handle includes
#(r"^```([a-zA-Z0-9.#+-]+)$.+^```$",					syntaxHylyter)]		#syntax highlighter OBSOLETE?

#pandoc has its own syntax highlighter (kate?), but it doesn't recognise AHK, or provide line numbering

"""
detects markdown links to other local articles, and sticks a .html on the end,
so rendered articles can link to other rendered articles
"""
def preProcess(inFile):
	#outFile = sys.argv[1]
	outFile = inFile
	# make sure that handleIncludes is executed before syntaxHylyter,
	# so that syntaxHylyter has something to work on for included files
	for rule in conversionRules: #( handleTagList, handleIncludes, syntaxHylyter):
		pat = re.compile(rule[0], re.MULTILINE)
		outFile = pat.sub(rule[1], outFile)
		#outFile = converter(outFile)
	return outFile
