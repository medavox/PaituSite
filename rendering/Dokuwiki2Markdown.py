#!/usr/bin/python

import re, os
"""
TODO:
-----
link internal [[pagename|Link text]] -> [Link Text](pagenameAsURL)
no-label link internal [[pagename]]
anchor internal link [[pagename#anchor|this Section]]

italic "//<italictext>//" -> "*<emph>*" or "_<emph>_" WITHOUT CLASHING WITH URLS
bold+italic "//**<boldtalic>**//" 	-> "***<strong>***" or "___<strong>___"
italic+bold "**//<boldtalic>//**" 	-> "***<strong>***" or "___<strong>___"

downloadable code blocks "<file <lang> <filename>> <sourcecode> </file>" -> ???
tag "{{tag><taglist>}} -> "%tag:<taglist>

DONE:
-----
Headings (h1 - h5)
footnote = "((footnote text))" -> "^[<inline footnote>]" (ext: inline_notes)
superscript "<super><text></super>" -> "^<text>^"
subscript "<sub><text></sub>" -> "~<text>~"
strikeout "<del><struck></del>" -> ~~<struck>~~" (ext: strikeout)

codeblock "<code><text></code>" -> "```\n<text>\n```", or "`<inline code>`"
codeblock languaged "<code <lang>><text></code>" -> "```<lang>\n<text>\n```"
monospace "''<mono>''" -> "`<mono>`"
indented monospace
link ext [[url|text]] -> [text](url)
TABLE HEADERS - the table pipe are the same
ordered list   "  - <text>" -> "<num>. <text>" or "#. <text>" (ext: fancy_lists)

identical (or do not need changing) markers:
-------------------------------------------
blockquote (seems to be the same)
horizontal rule "-{4,}" - > "-{3,}" (so it's basically fine)
bold "**<boldtext>**" 	-> "**<strong>**" or "__<strong>__"
unordered list "  * <text>" -> "* <text>"(dokuwiki lists are just-about-valid markdown lists)

BUGS:
* matched strings inside of escape characters are not ignored by this file. eg:

When you use the ''%%<code>%%'' or ''%%<file>%%'' syntax as above, you might want to make the shown code available for download as well. You can do this by specifying a file name after language code like this:

* a <code> tag wrapped around a <file> tag will, at best, produce two sets of of ``` fences; 
	one at the start, one at the end. At the moment though, something else is going on.
<code>
<file php myexample.php>
<?php echo "hello world!"; ?>
</file>
</code>

<file php myexample.php>
<?php echo "hello world!"; ?>
</file>
"""

footnote = 0
nohttp = r"[^h][^t][^t][^p][^:]"

def dashRepl(mo):
	out = ""
	for i in range(len(mo.group(0))):
		out = out + "-"
	return out

def tableConvert(mo):#matchObject
	#print mo.string
	#print mo.group(0)
	sploit = mo.group(0).replace('^', '|')
	headerline = re.sub(r"[0-9A-Za-z',.!? \t()]+", dashRepl, sploit)
	print headerline
	return sploit+"\n"+headerline
	
def footnoter(mo):
	global footnote
	footnote+=1
	fetnut = "[^"+str(footnote)+"]"
	return ""+fetnut+mo.group(2)+"\n"+fetnut+": "+mo.group(1)
	#r"[^"+str(footnote+=1)+"]\2\n[^"+str(footnote)+"]:\1"
	
"""
converts files embedded into dokuwiki documents with the <file> tag into standalone files, 
which are %included back into the document at compile time
"""
def unembedFile(mo):
	print "unembedder!"
	#group 1 = the language type
	#group 2 = the file name
	#group 3 = the file contents
	
	newPath = "../includes/"+mo.group(2)
	embeddedFile = open(newPath,'w')
	embeddedFile.write(mo.group(3))
	embeddedFile.close()
	
	language = mo.group(1)
	if language == "-":
		language = ""
	
	return "```"+language+"\n%include "+newPath+"\n```\n"

convOrig = \
[(r"^====== ?([\S \t]+) ?======$",	r"# \1\n"),			#headings
(r"^===== ?([\S \t]+) ?=====$", 	r"## \1\n"),
(r"^==== ?([\S \t]+) ?====$",		r"### \1\n"),
(r"^=== ?([\S \t]+) ?===$",			r"#### \1\n"),
(r"^== ?([\S \t]+) ?==$",			r"##### \1\n"),
(r"\(\(([\S \t]+)\)\)([\S \t]*)$",	footnoter),				#footnotes
(r"<sub>([\S \t]+)</sub>",			r"~\1~"),				#subscript
(r"<sup>([\S \t]+)</sup>",			r"^\1^"),				#superscript
(r"<del>([\S \t]+)</del>",			r"~~\1~~"),				#strikeout
#(r"\[\[(https?://[\w./?&=+,#-]+) ?\| ?([\S \t]+)\]\]", r"[\2](\1)"),#links with labeltext OLD
(r"\[\[([\w./:?&=+,#-]+) ?\| ?([^\]]+)\]\]", r"[\2](\1)"),#links with labeltext
(r"\[\[([^\]]+)\]\]",				r"<\1>"),				#links without labeltext
(r"(?<!http:)//([^/]+)//",			r"_\1_"),				#italic! (excepting http links)
(r"(?<!https:)//([^/]+)//",			r"_\1_"),				#italic! (excepting https links)
(r"\\\\[ \n]",						r"  \n"),				#forced linebreak
(r"<code ([\w.#+-]+)>((.|\n)+?)</code>", r"```\1\n\2\n```\n"),	#codeblock with language attribute
(r"<code>((.|\n)+?)</code>", 	r"\n```\n\1\n```\n"),		#codeblock without language attribute
#<file autohotkey TimeTracker-1.0.ahk>
(r"<file ([\w.#+-]+) ([^>]+)>((.|\n)+?)</file>", unembedFile),	#embedded <file> blocks to included seperate files
(r"''([^']+)''", 					r"`\1`"),				#monospace/inline code
(r"^  ([^-*][\S \t]+)$",			r"    \1"),				#indented monospace/inline code
(r"^([ \t]*)-( ?[\w])", 			r"\1#. \2"),			#numbered lists
(r"^([\t ]+)\*([\w])",				r"\1* \2"),				#unordered lists:add markdown-mandatory spaces which were optional in dokuwiki
(r"{{tag>([\w ,]+)}}",				r"\n%tags:\1\n"),		#tag list
(r"^\^ ?([\S \t]+\^)+$",			tableConvert)]			#table head match rule

#for cwd, dirs, files in os.walk('../import'):
for cwd, dirs, files in os.walk('../munge'):
	for f in files:
		if f[-4:] == '.txt':
			print("converting "+f)
			fyl = open(os.path.join(cwd,f), 'r')
			#fyl = open("../pages/almondmilk.txt", 'r')
			pageString = fyl.read()
			fyl.close()
			
			if re.search(re.compile(convOrig[0][0], re.M), pageString) == None: #promote second-level headings if no top-level headings exist in document
				conversionRules = [] #initialise empty list
				for i in range(1, 5): #1, 2, 3, 4
					conversionRules.append((convOrig[i][0], convOrig[i-1][1]))	#take the matching rule of headers h2 and below, and convert to h(n-1)
				conversionRules += convOrig[5:]			#append the rest of the normal rules onto the modified ruleset
			else:
				#print "loituma"
				conversionRules = convOrig
			
			#this is where it all gets done
			for rule in conversionRules:
				#print rule
				pat = re.compile(rule[0], re.M)
				pageString = pat.sub(rule[1], pageString)
			
			#converted = open(os.path.join("../converted", f[:-3]+"md"), 'w')
			converted = open(os.path.join("../articles", f[:-3]+"md"), 'w')
			converted.write(pageString)
			converted.close()
