#!/usr/bin/python
import re, sys


"""
replaces the %tag(s): command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
"""

posixPath = "" # todo: get code from home

def handleTagList(inFile):
	taglistpat = re.compile("^%tags?: ?([^,]+(,[^,])*)$", re.MULTILINE)
	return taglistpat.sub(tagLister, inFile)

def handleInternalLinks(inFile):
	linkpat = re.compile("(\[[^]]+\]\((?!http://)[^/])\)", re.MULTLINE)
	return linkpat.sub("\1\2.html\)", inFile)

def handleDogs(inFile):
	return inFile
	
def tagLister(matchObj):
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
	
outFile = sys.argv[1]
for converter in ( handleTagList, handleDogs ):
	outFile = converter(outFile)

print outFile
