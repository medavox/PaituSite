A modern Homespun Personal Site on the Paitu
============================================

The idea is to have a bunch of markdown files in some (hidden?) dir, then have them rendered to a static site

The site should have a menu, be responsive, and be as lightweight and performant as possible

Features
--------

* title generation
* tags
    - uses the special `%tags:` line, containing a comma-seperated list of tags, which can contain spaces

still to come:

* Internal links between articles
* special `%include` directive, to include the contents of a file inside the rendered copy of another
* date stamps
* Syntax highlighting

Posts will be:-

* date marked, and accessible by date
* searchable by content (hopefully, although that WILL require server-side scripting)
* searchable by tag cloud

* we're switching to nginx as the webserver;
	- it's becoming more popular than lighttpd,
	- is more actively developed,
	- and the config files make more sense to me
* We're going to use PureCSS for the responsive bit
* pandoc for the markdown->HTML rendering
* for now, just upload .md files to the mdfiles directory via SSH/rsync, then notify the renderer to update
	- may use a diffed last-copy system, so pandoc knows what files have changed/are new, based on the last rendered copy
	- may also used a once-a-minute timer for live edits, so we don't constantly re-trigger update (if they are even automatic)

Longer Term:
------------
* We'll need a syntax highlighter
* what to put in sidebar?
	- Tag List
	- About/Links (to my github, SO etc)
	- Other Blogs

TODO
----
* fix the fact that stripping out tags will mean the lastinput and mdffiles versions are always different
* able to link between different pages on blog
* Syntax Highlighting source code files, making them like in Dokuwiki
	- Download link for source code files in surrounding page
	- annotatable with prose on the html page, which is 'outside' the source code file
		- create an %include command, which displays the contents of another file (the source code) in a given page
* Date page written, and/or date last updated
* Multiple Author support?
* put generated tag pages in their own directory?

DONE
----
* The tags (if any) a page has are added as a list of links to the bottom of that page
* Clickable list of articles with a given tag
