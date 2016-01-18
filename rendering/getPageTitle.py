import sys, re

def getTitle(filename):
	openMd = open(filename, 'r')
	#contents = openMd.read()
	contents = openMd.readline() + openMd.readline() #get first two lines as a str; basically head -n 2
	#print contents
	pat = re.compile('^(.+)\n===+$', re.M)
	suche = pat.search(contents)
	#print suche
	if not suche == None:
		return suche.group(1)
	else:
		#return filename[11:-3]
		nopath = filename.split("/")[-1]
		return nopath[:-3]
if len(sys.argv) < 2:
	print "ERROR: need at least one arg!"
	sys.exit()
print getTitle(sys.argv[1])
