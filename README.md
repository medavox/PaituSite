Jekyll's Skinnier Cousin
========================


* Generate static blog sites from markdown for a super-fast, super-lightweight blogging platform.
	- Uses no PHP (or execution of any kind) on the webserver, 
	and very little javascript on the client (browser). Everyone gets a fast experience!
	- it's just text!
* You write some markdown, and you really do get that nice, no-maintenance blog you always wanted.
* Written in python and bash, so it's even easy to install and run. *cough* jekyll *cough*

* Uses [solid software under the hood](#builton), so none of us (bloggers, readers, developers) have to reinvent the wheel.

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

<a name="builton"></a>Built Using
-----------

* Pandoc for the markdown-to-HTML rendering
* SOON: Pygments for code syntax highlighting!
* PureCSS for the responsive stuff & sidebar
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
* put labelled box around `%include`d code, with a clickable link (the filename) to download it
	- also insert language next to markdown code fence, if detectable
* nicer anchor links support (less html-y, more markdownish) than standard markdown
* fix the fact that stripping out tags will mean the lastinput and mdfiles versions are always different
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

Only activate syntax highlighting inside fenced blocks with a named language, eg:


	```java

	public class Foo
	{
	...
	}
	```


DONE
----
* The tags (if any) a page has are added as a list of links to the bottom of that page
* Clickable list of articles with a given tag
* special `%include` directive, to include the contents of a file inside the rendered copy of another

%tags: readme
