#!/usr/bin/python
import re, sys

posixPath = "([^/]+/)*/?[^/]*\.[a-zA-Z0-9]{1,10}" # todo: get code from home

"""
handles any remaining in-place article substitutions, before sending to pandoc.

such as:

* the %include command,
* making internal links work (todo)

"""
def handleIncludes(inFile): # posix path regex:
	#regexplanation:
	# at the beginning of a line: 0 or more (1 or more non-slashes followed by a slash),
	# followed by 0 or more nonslashes (the filename),
	# followed by a dot, then 1-10 ascii latin characters (the file extension). End of line.
	# extensionless files are not supported, because they usually don't show up on the internet,
	# and if they did, they would be suspicious anyway
	
	pat = re.compile(r"^%include ("+posixPath+")$", re.MULTILINE)
	return pat.sub(includer, inFile)

def includer(matchObj):
	#print "ding!"
	includingFileName = matchObj.group(1)
	print "found file name:"+includingFileName
	openedFile = open(includingFileName, 'r')
	return openedFile.read()

"""
replaces the %tag(s): Paitu command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
"""
def handleTagList(inFile):
	#taglistpat = re.compile(r"^%tags?: ?([^,\n]+(,[^,\n])*)$", re.MULTILINE)
	taglistpat = re.compile(r"^%tags?: ?([^,]+(,[^,]+)*)$", re.MULTILINE)
	return taglistpat.sub(tagLister, inFile)

"""
the actual regex function for creating lists of tags, which generates the markdown
"""
def tagLister(matchObj):
	print "taglister"
	rawTags = matchObj.group(1)
	pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
	cleanedCommas = pat.sub( ',', rawTags)
	
	#tagfoot = "<p>Tagged as: " # html-output version
	tagfoot = "\n\nTagged as: " # markdown-output
	for tag in cleanedCommas.split(','):
		#tagfoot += "<a href="+tag.replace(' ', "%20")+".html>"+tag+"</a> " # html
		tagfoot += "["+tag+"]("+tag.replace(' ', "%20")+".html) " # markdown
	#tagfoot += "</p>"
	return tagfoot+"\n"


#TODO: unfinished
"""
detects markdown links to other local articles, and sticks a .html on the end,
so rendered articles can link to other rendered articles
"""
def handleInternalLinks(inFile):
	#linkpat = re.compile('(\[.+\]\()((?!http://)[^/])\)')
	"""regexplanation:
	
	"""
	linkpat = re.compile("(\[[^\]\n]+\]\((?!http://)"+posixPath+")\)", re.MULTILINE)
	return linkpat.sub('\1\2.html\)', inFile)
	
#TODO: unfinished
"""
detects language-labelled code fence blocks, eg:

```java

blahjava

```
and runs pygments on them.
"""
def syntaxHylyter(inFile):
	codepat = re.compile(r"^```([a-zA-Z0-9.#+-]+)$.+^```$", re.MULTILINE)
	
	return inFile



#----------commandline runtime

outFile = sys.argv[1]
# make sure that handleIncludes is executed before syntaxHylyter,
# so that syntaxHylyter has something to work on for included files
for converter in ( handleTagList, handleIncludes, syntaxHylyter):
	outFile = converter(outFile)

print outFile
