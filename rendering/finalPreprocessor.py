#!/usr/bin/python
import re, sys

inputFile = sys.argv[1]

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
