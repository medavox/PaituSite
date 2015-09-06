#!/usr/bin/python
import os, sys, re
 
#if len(sys.argv) < 2:
#	print "usage:" + sys.argv[0] +  """<dir>
#	where <dir> is a root dir of files you wish to analyse recursively."""
#	sys.exit(0)

tagDict = dict()

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
tagEntries = open('./tagEntries.html', 'w')
for tag in tagDict.keys():
	print tag
	#consider sorting tags before printing
	linkUrl = ""+tag+'.html'
	tagEntries.write('\n\t\t\t\t\t<li class=\"pure-menu-item\">\n\t\t\t\t\t\t<a href=\"'+linkUrl+
		'" class="pure-menu-link">'+tag+'</a>\n\t\t\t\t\t</li>')
tagEntries.close()

#generate the markdown for pages containing a list of 
