#!/usr/bin/python

import re, os
"""
link ext [[url|text]] -> [text](url)
link int [[pagename|Link text]]
link int [[pagename]]
anchor internal link [[pagename#anchor|this Section]].

unordered list "  * <text>" -> "* <text>"
ordered list   "  - <text>" -> "<num>. <text>" or "#. <text>" (ext: fancy_lists)

footnote = "((footnote text))" -> "^[<inline footnote>]" (ext: inline_notes)

codeblock "<code><text></code>" -> "```\n<text>\n```", or "`<inline code>`"
codeblock languaged "<code <lang>><text></code>" -> "```<lang>\n<text>\n```"

italic "//<italictext>//" -> "*<emph>*" or "_<emph>_"
bold "**<boldtext>**" 	-> "**<strong>**" or "__<strong>__"
bold+italic "//**<boldtalic>**//" 	-> "***<strong>***" or "___<strong>___"
strikeout "<del><struck></del>" -> ~~<struck>~~" (ext: strikeout)
monospace "''<mono>''" -> "`<mono>`"

superscript "<super><text></super>" -> "^<text>^"
subscript "<sub><text></sub>" -> "~<text>~"

identical (or do not need changing) markers

blockquote (seems to be the same)
horizontal rule "-{4,}" - > "-{3,}" (so it's basically fine)

Dokuwiki:

^ Heading 1      ^ Heading 2       ^ Heading 3          ^
| Row 1 Col 1    | Row 1 Col 2     | Row 1 Col 3        |
| Row 2 Col 1    | some colspan (note the double pipe) ||
| Row 3 Col 1    | Row 3 Col 2     | Row 3 Col 3        |


Markdown (ext: pipe_tables):

heading 1		| heading 2			| heading 3
----------------|-------------------|-----------
row 1 col 1		| row 1 col 2		| row 1 col 3
row 2 col 1		| colspan??		| row 1 col 3
row 3 col 1		| row 3 col 2		| row 3 col 3

h1 "====== <text> ======" -> "# <text>"
h2 "===== <text> =====" -> "## <text>"
h3 "==== <text> ====" -> "### <text>"
h4 "=== <text> ===" -> "#### <text>"
h5 "== <text> ==" -> "##### <text>"


downloadable code blocks "<file <lang> <filename>> <sourcecode> </file>" -> ???
tag "{{tag><taglist>}} -> "%tag:<taglist>
"""

conversionRules = \
[(r"^====== ?([\S \t]+) ?======$", r"# \1"),					#headings
(r"^===== ?([\S \t]+) ?=====$", r"## \1"),
(r"^==== ?([\S \t]+) ?====$", r"### \1"),
(r"^=== ?([\S \t]+) ?===$", r"#### \1"),
(r"^== ?([\S \t]+) ?==$", r"##### \1"),
(r"\(\(([\S \t]+)\)\)", r"\^\[\1\]"),							#footnotes
(r"<sub>([\S \t]+)</sub>", r"~\1~"),							#subscript
(r"<super>([\S \t]+)</super>", r"~\1~"),						#superscript
(r"<del>([\S \t]+)</del>", r"~~\1~~"),							#strikeout
(r"<code (.+)>([\S \n\t]+)</code>", r"```\1\n\2\n```\n"),		#codeblock with language attribute
(r"<code>(.+)</code>", r"\n```\n\1\n```\n"),					#codeblock without language attribute
(r"''([\S \t]+)''", r"`\1`"),									#monospace/inline code
(r"^  ([^-*][\S \t]+)$", r"    \1"),							#indented monospace/inline code
#(r"//([\S \t]+)//", r"*\1*"),									#italic; match pattern currently broken
(r"\[\[(https?://[a-zA-Z-_./?&=0-9+,#]+)\|([A-Za-z0-9 ]+)\]\]", r"[\2](\1)"),#links with labeltext
(r"\[\[(https?://[a-zA-Z-_./?&=0-9+,#]+)\]\]", r"<\1>"),		#links without labeltext
(r"^([ \t]*)-( ?[\w])", r"\1#. \2"),							#numbered lists
#(r"^(  \*([\w])", r"\* \1"),									#tidying unordered lists
(r"^\^ ?([\S \t]+\^)+$", r""),										#tables:headers
#(r"^(\^ ?([\S \t])+)+", r"\2"),								#tables:headers
#(r"^\^ ?", r"| "),												#tables:remove starting ^ in headers
#(r"(([\S \t])+)+\^", r"\1|"),									#tables:convert header from ^ to |
#(r"([\S \t])+\^.*$", r"\=|---"),								#tables:a from ^ to |
#tables:generate header pipe row
(r"{{tag>([a-zA-Z ,]+)}}", r"\n%tags:\1\n")]					#tag list
#(r"^{{tag>(.*) (.*)}}", r"\n%tags:\1,\2\n")]						#tag list
#unordered list
#tables...

#("**([\S \t]+)*","**\1**"),									#bold is the same: **<bold>**
#(r"<code(.?( [a-zA-Z]+)?)>([\S \t]+)</code>", r"\n```\1\n\2\n```\n"),#codeblock with optional language attribute
#(r"<code(.?( [a-zA-Z]+)?)>([\S \t]+)</code>", r"\n```\1\n\2\n```\n"),#codeblock with optional language attribute
#conversionRules = [(r"^====== ?([A-Za-z 0-9:-]+) ?======$", r"# \1\n\n")]

#print "Lol"

def tableConvert(matchObject):
	print string
	tokens = matchObject.string.split('^')
	output = ""
	for token in tokens:
		output = output + token + ("|" if tokens[-1] == token else "")
	return output
	#string.replace("{{
	#pat = re.compile("", re.M)

def tagConvert(matchObject):
	

for cwd, dirs, files in os.walk('../pages'):
	for f in files:
		if f[-3:] == 'txt':
			print("converting "+f)
			fyl = open(os.path.join(cwd,f), 'r')
			#fyl = open("../pages/almondmilk.txt", 'r')
			pageString = fyl.read()
			fyl.close()
			for rule in conversionRules:
				print rule
				pat = re.compile(rule[0], re.M)
				#mo = pat.search(pageString)
				#print mo
				#print mo.groups()
				pageString = re.sub(pat, rule[1], pageString)
			pati  = re.compile(r"^\^ ?([\S \t]+\^)+$", re.M) #table head match rule
			patty = re.compile(r"^\^ ?([\S \t]+\^)+$", re.M) #table head match rule
			pageString = re.sub(pat, tableConvert, pageString)
			
			converted = open(os.path.join("../converted", f[:-3]+"md"), 'w')
			converted.write(pageString)
			converted.close()
