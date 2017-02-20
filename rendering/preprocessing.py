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

NO_MODE = 0
TAG_MODE = 1
AUTHOR_MODE = 2

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
replaces the '%tag(s):' Paitu command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
the actual regex function for creating lists of tags, which generates the markdown
"""
def tagLister(matchObj):
	#print "taglister"
	directive = matchObj.group(1)
	if "tag" in directive and not "author" in directive:
		mode = TAG_MODE
	elif "author" in directive and not "tag" in directive:
		mode = AUTHOR_MODE
	#else:
	#	mode = NO_MODE
	rawTags = matchObj.group(2)
	pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
	cleanedCommas = pat.sub( ',', rawTags)

	if mode == TAG_MODE:
		tagfoot = "\n\nTagged as: " # markdown-output
	elif mode == AUTHOR_MODE:
		tagfoot = "\nBy "
	for tag in cleanedCommas.split(','):
		tagfoot += "["+tag+"]("+directive+"s/"+cleanTitle(tag) + ".html) " # markdown
	return tagfoot+"\n"

"""
Converts Ysgrifen's wiki-style internal links into functioning HTML links
"""
def internalLinker(matchObj):
	#print matchObj.group(1) #[case-insensitive internal link](
	#print matchObj.group(2) #<the path before the filename in the link 'url'>
	#print matchObj.group(3) #chat bOt project
	out = matchObj.group(1)
	linkName = matchObj.group(2).lower().replace(' ', '_')
	return out +linkName+".html)"#+"LINKA!GROVE!"

#[(r"^%tags?: ?([^\n,]+(,[^\n,]+)*) *$", 				tagLister),			#handle tag list -- pre-author addition
conversionRules = \
[(r"^%(tag|author)s?: ?([^\n,]+(,[^\n,]+)*) *$", 		tagLister),			#processes tag lists
 (r"(\[[^\]\n]+\]\()([\w _-]+)\)", 						internalLinker), 	#handles wiki-style internal links
 (r"^<a:([\w-]+)>",										r'<a name="\1"></a>'),#expands shortened anchor syntax to full html # TODO
 (r"^%include (([^/]+/)*/?[^/]*\.[a-zA-Z0-9]{1,10})$",	includer)]			#processes %include directives
#(r"^```([a-zA-Z0-9.#+-]+)$.+^```$",					syntaxHylyter)]		#syntax highlighter OBSOLETE?

#pandoc has its own syntax highlighter (kate?), but it doesn't recognise AHK, or provide line numbering

"""
detects markdown links to other local articles, and sticks a .html on the end,
so rendered articles can link to other rendered articles
"""
def preProcess(inFile):
	outFile = inFile
	for rule in conversionRules:
		pat = re.compile(rule[0], re.MULTILINE)
		outFile = pat.sub(rule[1], outFile)
	return outFile
