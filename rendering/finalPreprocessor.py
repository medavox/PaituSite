#!/usr/bin/python
import re, sys

inputFile = sys.argv[1]


"""
replaces the %tag(s): command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
"""
def handleTagList(inFile):
	taglistpat = re.compile("^%tags?: ?([^,]+(,[^,])*)$", re.MULTILINE)
	return taglistpat.sub(tagLister, inFile)
	
			
	
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
	
outputFile = handleTagList(inputFile)#
print outputFile
