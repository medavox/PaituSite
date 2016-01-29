#!/usr/bin/python
import os, sys, re
#from render import getTitle

"""
Creates a page for each tag, with links to each article with that tag.
Tags are found by checking all articles
"""
tagDict = dict()

def getTags(filename):
	openfile = open(filename, 'r')
	contents = openfile.read()
	pat = re.compile(r"^%tags?: ?([^,]+(,[^,]+)*)$")
	retlist = []
	for mo in pat.finditer(contents, re.M):
		rawTags = mo.group(1)
		pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
		cleanedCommas = pat.sub( ',', rawTags)
		retlist = retlist + cleanedCommas.split(',')
	return retlist

#generate navbar links to tag pages, as an add-in snippet
#generate the markdown for tag pages
def parseTags(nope):
	#parse %tags, creating a global one-to-many associative array (dictionary) of tags to pages
	for f in os.listdir("../articles"):
		if f[-3:] == '.md':
			tagList = getTags("../articles/"+f)
			#print f+":"+str(type(tagList))
			if type(tagList) is list:
				for tag in tagList:
					if tag in tagDict:
						#add this file's name to listvalue of this tagkey
						tagDict[tag].append(f)
					else: #initialise this tagkey with a new list containing this filename
						tagDict[tag] = [f]
	
	#tagEntries = open('../temp/all_tags.html', 'w')
	#tagEntries.write("# All Tags\n")
	
	#create a page for every found tag.
	#on that page, add a link to every article with that tag
	for tag in tagDict.keys():
		#consider sorting tags before printing
	#	linkUrl = ""+tag
	#	tagEntries.write("* "+tag+"\n")
	#	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
	#		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
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
