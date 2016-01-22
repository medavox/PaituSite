A modern Homespun Personal Site on the Paitu
============================================

The idea is to have a bunch of markdown files in some (hidden?) dir, then have them rendered to a static site

The site should have a menu, be responsive, and be as lightweight and performant as possible

Features
--------

* Works out a title for each article, for pandoc to use in the `<title>` tag
* Uses a custom pandoc html template
* Article tags
    - uses the special `%tags:` line, containing a comma-seperated list of tags, which can contain spaces
    - also generates a page for each tag, listing all the articles with that tag
* Caches the last-rendered input (in lastinput/), so it knows which files have changed/are new since the last run
* An %include command, which includes the contents of another file (eg source code) in a given rendered page
	- usage: `%include path/to/file.ext` on its own line. Files must have an extension, because otherwise they'd appear too dodgy for the internet

###still to come:

* Internal links between articles
* date stamps
* Syntax highlighting

Posts will be:-

* date marked, and accessible by date

Built Using
-----------

* PureCSS for the responsive stuff & sidebar
* Pandoc for the markdown-to-HTML rendering
* Lots of regular expressions
* Some standard GNU console programs (diff, grep, head, tail, cat, echo, cp, mv...)
* Scripted using Bash 4 and Python 2
* That's it!


Usage
---

Just upload/update your Markdown files in mdfiles/ (via SSH/rsync?), then run rendering/render.sh
	

Longer Term:
------------
* Syntax highlighter for arbitrary source code
* what to put in sidebar?
	- Tag List
	- About/Links (to my github, SO etc)
	- Other Blogs

TODO
----
* fix the fact that stripping out tags will mean the lastinput and mdffiles versions are always different
* Link between different pages on blog
* Syntax Highlighting source code files, making them like in Dokuwiki
	- Download link for source code files in surrounding page
	- annotatable with prose on the html page, which is 'outside' the source code file
* Date page written, and/or date last updated
* Multiple Author support?
* put generated tag pages in their own directory?
* clean up the messy collab between bash and python
	- replace all bash usage with python? problems:
		* head, tail, diff
		* calling pandoc
		* moving, copying & removing files
	- replace 2nd phase of render.sh with python?
		* same
	- recombine python code into fewer files
		* how to then call python functions from bash? 
		* probably doable more neatly than currently
		* `RESULT=$(python -c 'import test; print test.get_foo()')`

DONE
----
* The tags (if any) a page has are added as a list of links to the bottom of that page
* Clickable list of articles with a given tag
* special `%include` directive, to include the contents of a file inside the rendered copy of another

%tags: readme
