#!/usr/bin/python
import re, sys

#handle includes regexplanation:
# at the beginning of a line: 0 or more of: (1 or more non-slashes followed by a slash),
# followed by 0 or more nonslashes (the filename),
# followed by a dot, then 1-10 ascii latin characters (the file extension). End of line.
# extensionless files are not supported, because they usually don't show up on the internet,
# and if they did, they would seem suspicious anyway

#taglistpat = re.compile(r"^%tags?: ?([^,\n]+(,[^,\n])*)$", re.MULTILINE)
	#linkpat = re.compile('(\[.+\]\()((?!http://)[^/])\)')

tagDict = dict()

"""
handles any remaining in-place article substitutions, before sending to pandoc.

such as:

* the %include command,
* making internal links work (todo)
"""
def includer(matchObj):
	#print "includer"
	includingFileName = matchObj.group(1)
	#print "found file name:"+includingFileName
	openedFile = open(includingFileName, 'r')
	return openedFile.read()

"""
replaces the %tag(s): Paitu command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
the actual regex function for creating lists of tags, which generates the markdown
"""
def tagLister(matchObj):
	#print "taglister"
	rawTags = matchObj.group(1)
	pat = re.compile(' ?, ?') #remove any spaces before or after the separating comma; but keep tag-internal spaces
	cleanedCommas = pat.sub( ',', rawTags)
	
	#tagfoot = "<p>Tagged as: " # html-output version
	tagfoot = "\n\nTagged as: " # markdown-output
	for tag in cleanedCommas.split(','):
		#tagfoot += "<a href="+tag.replace(' ', "%20")+".html>"+tag+"</a> " # html
		tagfoot += "["+tag+"]("+tag.replace(' ', "_").lower() + ".html) " # markdown
	#tagfoot += "</p>"
	return tagfoot+"\n"

#def internalLinker(matchObj):
	#print "LINKA!"
	#group(0) #the whole match: [case-insensitive internal link](chat bOt project)
	#print matchObj.group(1) #[case-insensitive internal link](
	#print matchObj.group(2) #<the path before the filename in the link 'url'>
	#print matchObj.group(3) #chat bOt project
#	out = matchObj.group(1)
	
#	if matchObj.group(2) is str:
#		out += matchObj.group(2)
	
#	linkName = matchObj.group(3).lower().replace(' ', '_')
	
#	return out +linkName+".html)"+"LINKA!GROVE!"
	
def internalLinker(matchObj):
	#print "LINKA!"
	#group(0) #the whole match: [case-insensitive internal link](chat bOt project)
	#print matchObj.group(1) #[case-insensitive internal link](
	#print matchObj.group(2) #<the path before the filename in the link 'url'>
	#print matchObj.group(3) #chat bOt project
	out = matchObj.group(1)
	
	linkName = matchObj.group(2).lower().replace(' ', '_')
	
	return out +linkName+".html)"#+"LINKA!GROVE!"
	

conversionRules = \
[(r"^%tags?: ?([^,]+(,[^,]+)*)$", 						tagLister),			#handle tag list
#(r"(\[[^\]\n]+?\]\((?!https?:/)/?([^/]+/)*)([^./]*)\)", internalLinker),	#handle internal links TODO
#(r"(\[[^\]\n]+\]\()(?<!http:/)/?([^/]+/)*([^./]+)\)", internalLinker),	#handle internal links TODO
 (r"(\[[^\]\n]+\]\()([\w ]+)\)", 						internalLinker),
#(r"^<a:([a-zA-Z0-9 _-?!,.]+)>",						r"<a name=\"\1\"></a>"),#expand shortened anchor syntax to full html
(r"^%include (([^/]+/)*/?[^/]*\.[a-zA-Z0-9]{1,10})$",	includer)]			#handle includes
#(r"^```([a-zA-Z0-9.#+-]+)$.+^```$",					syntaxHylyter)]		#syntax highlighter OBSOLETE?

"""
detects markdown links to other local articles, and sticks a .html on the end,
so rendered articles can link to other rendered articles
"""

outFile = sys.argv[1]
# make sure that handleIncludes is executed before syntaxHylyter,
# so that syntaxHylyter has something to work on for included files
for rule in conversionRules: #( handleTagList, handleIncludes, syntaxHylyter):
	pat = re.compile(rule[0], re.MULTILINE)
	outFile = pat.sub(rule[1], outFile)
	#outFile = converter(outFile)

print outFile
