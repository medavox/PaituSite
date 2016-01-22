#!/usr/bin/python
import re, sys




posixPath = "" # todo: get code from home
"""
replaces the %tag(s): Paitu command with markdown of links to the tag pages.
  html string of the tags for a given article, as links to the tag pages.
"""
def handleTagList(inFile):
	taglistpat = re.compile("^%tags?: ?([^,\n]+(,[^,\n])*)$", re.MULTILINE)
	return taglistpat.sub(tagLister, inFile)


#TODO: unfinished
"""
detects markdown links to other local articles, and sticks a .html on the end,
so rendered articles can link to other rendered articles
"""
def handleInternalLinks(inFile):
	linkpat = re.compile("(\[[^]\n]+\]\((?!http://)[^/\n])\)", re.MULTILINE)
	return linkpat.sub("\1\2.html\)", inFile)

def handleDogs(inFile):
	return inFile
	
"""
detects language-labelled code fence blocks, eg:
```java

blahjava

```

and runs pygments on them.
"""
def syntaxHylyter(inFile):
	codepat = re.compile("^```([a-zA-Z0-9.#+-]+)$.+^```$", re.MULTILINE)
	
	return inFile

"""
the actual regex function for creating lists of tags, which generates the markdown
"""
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


#----------commandline runtime

outFile = sys.argv[1]
# make sure that handleIncludes is executed before syntaxHylyter,
# so that syntaxHylyter has something to work one for included files
for converter in ( handleTagList, syntaxHylyter, handleDogs ):
	outFile = converter(outFile)

print outFile
