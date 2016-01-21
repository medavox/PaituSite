#!/usr/bin/python
import sys, re

def getTags(filename):
	openfile = open(filename, 'r')
	for line in openfile.readlines():
		if line.startswith("%tag") and ':' in line:#make sure the "%tag" line contains a ":"
			tagString = line[line.index(':')+1:]#remove the leading "%tag:" from the start of line
			pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
			cleanedCommas = pat.sub( ',', tagString)
			if cleanedCommas[-1] == '\n':
				cleanedCommas = cleanedCommas[:-1] #strip trailing newline
			#print tagString
			#tagList = 
			openfile.close()
			return cleanedCommas.split(',')


if __name__=='__main__':
	if len(sys.argv) < 2:
		print "ERROR: need at least one arg!"
		sys.exit()
		#else
	tagList = getTags(sys.argv[1])
	if type(tagList) is list:
		for tag in tagList:
			print tag
	#print getTags(sys.argv[1])
