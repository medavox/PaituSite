#!/usr/bin/python
import sys, re

"""
returns the derived title of a given mdfile, whether from its markdown title, or its file name.
works in both python and bash.

python usage:

	from getPageTitle import getTitle

	...

	title = getTitle("../articles/lol.md")

bash usage:

	title=$(./getPageTitle.py ../articles/lol.md)
"""

def getTitle(filename):
	openMd = open(filename, 'r')
	#contents = openMd.read()
	contents = openMd.readline() + openMd.readline() #get first two lines as a str; basically head -n 2
	#print contents
	pat = re.compile('^(.+)\n===+$', re.MULTILINE)
	suche = pat.search(contents)
	#print suche
	if not suche == None:
		return suche.group(1)
	else: #if the article text contains no discernible title, use the file name
		nopath = filename.split("/")[-1]
		if nopath.endswith(".md"):
			return nopath[:-3]
		else:
			return nopath


if __name__=='__main__':
	if len(sys.argv) < 2:
		print "ERROR: need at least one arg!"
		sys.exit()
		#else
	print getTitle(sys.argv[1])
