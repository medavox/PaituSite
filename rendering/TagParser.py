#!/usr/bin/python
import os, sys, re
from getPageTitle import getTitle
 
#if len(sys.argv) < 2:
#	print "usage:" + sys.argv[0] +  """<dir>
#	where <dir> is a root dir of files you wish to analyse recursively."""
#	sys.exit(0)

tagDict = dict()

#todo: add list of tags a page has to the bottom of that page

#recursively walks a file tree, from a given directory down
for cwd, dirs, files in os.walk('../mdfiles'):
	for f in files:
		if f[-3:] == '.md':
			openfile = open(os.path.join(cwd,f), 'r')
			#add stuff here
			for line in openfile.readlines():
				if line.startswith("%tag"):
					colonIndex = line.find(':')
					if(colonIndex != -1): #make sure the line starting with "%tag" actually contains a ":"
						tagString = line[colonIndex+1:]
						pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
						cleanedCommas = pat.sub( ',', tagString)
						if cleanedCommas[-1] == '\n':
							cleanedCommas = cleanedCommas[:-1] #strip trailing newline
						#print tagString
						tagList = cleanedCommas.split(',')
						for tag in tagList:
							if tag in tagDict:
								#add this file's name to listvalue of this tagkey
								tagDict[tag].append(f)
							else:
								#initialise this tagkey with a new list containing this filename
								tagDict[tag] = [f]
			openfile.close()

#generate navbar links to tag pages, as an add-in snippet
tagEntries = open('../html/tagEntries.html', 'w')
for tag in tagDict.keys():
	#print tag
	#consider sorting tags before printing
	linkUrl = ""+tag+'.html'
	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
	tagPage = open('../temp/'+tag+'.md', 'w')
	tagPage.write("Pages Tagged '"+tag+"'\n===\n\n") # write page title
	for page in tagDict[tag]:
		link = page.lower().replace(' ', '_')[:-3]+".html"
		title = getTitle("../mdfiles/"+page)
		#if title == "":			#if the article text contains no discernible title, use the file name
		#	title = page[:-3]
		tagPage.write("* ["+title+"]("+link+")\n")
		#pass
		print tag+":"
		print "\t\""+title+"\" at "+link
	tagPage.close()
	
tagEntries.close()

#getTitle('../mdfiles/Chat bot project.md')
#generate the markdown for tag pages

#[This is an example inline link](http://www.duckduckgo.com "Example Title")
#the link label should be the page title,
#or failing that, the file name
