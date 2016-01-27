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
"""

def dashRepl(mo):
	out = ""
	for i in range(len(mo.group(0))):
		out = out + "-"
	return out

def tableConvert(mo):#matchObject
	#print mo.string
	#print mo.group(0)
	#print "alalflala"
	sploit = mo.group(0).replace('^', '|')
	headerline = re.sub(r"[0-9A-Za-z',.!? \t()]+", dashRepl, sploit)
	print headerline
	return sploit+"\n"+headerline

convOrig = \
[(r"^====== ?([\S \t]+) ?======$",		r"# \1\n"),				#headings
(r"^===== ?([\S \t]+) ?=====$", 		r"## \1\n"),
(r"^==== ?([\S \t]+) ?====$",			r"### \1\n"),
(r"^=== ?([\S \t]+) ?===$",				r"#### \1\n"),
(r"^== ?([\S \t]+) ?==$",				r"##### \1\n"),
(r"\(\(([\S \t]+)\)\)", 				r"\^\[\1\]"),			#footnotes
(r"<sub>([\S \t]+)</sub>",				r"~\1~"),				#subscript
(r"<super>([\S \t]+)</super>",			r"~\1~"),				#superscript
(r"<del>([\S \t]+)</del>",				r"~~\1~~"),				#strikeout
(r"\[\[(https?://[a-zA-Z-_./?&=0-9+,#]+) ?\| ?([\S \t]+)\]\]", r"[\2](\1)"),#links with labeltext
(r"\[\[(https?://[a-zA-Z-_./?&=0-9+,#]+)\]\]",	r"<\1>"),		#links without labeltext
(r"(?<!http:)//([^/]+)//",				r"_\1_"),				#italic!
#(r"//\*\*[^ ]([\S \t]+)[^ ]\*\*//", 	r""),					#italic-bold
#(r"\*\*//[^ ]([\S \t]+)[^ ]//\*\*",	r""),					#bold-italic
(r"\\\\[ \n]",							r"  \n"),				#forced linebreak
(r"<code (.+)>([\S \n\t]+)</code>", 	r"```\1\n\2\n```\n"),	#codeblock with language attribute
(r"<code>(.+)</code>", 					r"\n```\n\1\n```\n"),	#codeblock without language attribute
(r"''([^']+)''", 						r"`\1`"),				#monospace/inline code
(r"^  ([^-*][\S \t]+)$",				r"    \1"),				#indented monospace/inline code
(r"^([ \t]*)-( ?[\w])", 				r"\1#. \2"),			#numbered lists
(r"^([\t ]+)\*([\w])",					r"\1* \2"),				#tidying unordered lists:add markdown-mandatory spaces which were optional in dokuwiki
(r"{{tag>([a-zA-Z ,]+)}}",				r"\n%tags:\1\n"),		#tag list
(r"^\^ ?([\S \t]+\^)+$",				tableConvert)]			#table head match rule

#unordered list
#(r"<code(.?( [a-zA-Z]+)?)>([\S \t]+)</code>", r"\n```\1\n\2\n```\n"),#codeblock with optional language attribute
#conversionRules = [(r"^====== ?([A-Za-z 0-9:-]+) ?======$", r"# \1\n\n")] # test for matching text with punctuation

	
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
