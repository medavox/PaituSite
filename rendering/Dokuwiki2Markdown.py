import re
"""
link ext [[http://www.google.com|This Link points to google]]
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

superscript
subscript

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

heading1 = re.compile("")

