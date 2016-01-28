#!/usr/bin/python
import os, sys, re
from getPageTitle import getTitle
#from finalPreprocessor import getTags

"""
Creates a page for each tag, with links to each article with that tag.
Tags are found by checking all articles
"""

#if len(sys.argv) < 2:
#	print "usage:" + sys.argv[0] +  """<dir>
#	where <dir> is a root dir of files you wish to analyse recursively."""
#	sys.exit(0)

tagDict = dict()

def getTags(filename):
	openfile = open(filename, 'r')
	for line in openfile.readlines():
		if line.startswith("%tag") and ':' in line:#make sure the "%tag" line contains a ":"
			tagStartIndex = line.index(':')+1
			if line[tagStartIndex] == ' ':
				tagStartIndex = tagStartIndex +1
			tagString = line[tagStartIndex:]#remove the leading "%tag:" from the start of line
			pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
			cleanedCommas = pat.sub( ',', tagString)
			if cleanedCommas[-1] == '\n':
				cleanedCommas = cleanedCommas[:-1] #strip trailing newline
			#print tagString
			#tagList = 
			openfile.close()
			return cleanedCommas.split(',')

for cwd, dirs, files in os.walk('../articles'):
	for f in files:
		if f[-3:] == '.md':
			#parse %tags, creating a global one-to-many associative array (dictionary) of tags to pages
			tagList = getTags(os.path.join(cwd,f))
			#print f+":"+str(type(tagList))
			if type(tagList) is list:
				for tag in tagList:
					if tag in tagDict:
						#add this file's name to listvalue of this tagkey
						tagDict[tag].append(f)
					else: #initialise this tagkey with a new list containing this filename
						tagDict[tag] = [f]

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
tagEntries = open('../temp/tagEntries.html', 'w')
tagEntries.write("All Tags\n===\n")
for tag in tagDict.keys():
	#print tag
	#consider sorting tags before printing
	linkUrl = ""+tag
	tagEntries.write("* "+tag+"\n")
	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
	tagPage = open('../temp/'+tag.replace(' ', '_').lower()+'.md', 'w')
	#tagPage.write("Pages Tagged '"+tag+"'\n===\n\n") # write page title
	for page in tagDict[tag]:
		link = page.lower().replace(' ', '_')[:-3]+".html"
		title = getTitle("../articles/"+page)
		tagPage.write("* ["+title+"]("+link+")\n")
		print tag+":"
		print "\t\""+title+"\" at "+link
	tagPage.close()
	
tagEntries.close()
