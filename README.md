Ysgrifen 
========

*(Pronounced us-GREE-ven)*

A Tiny Static Site Generator With Cool Features
----------------------


* Write your articles in [Markdown](http://commonmark.org/) for a super-fast, super-lightweight blogging platform.
	- Executes nothing on the webserver per-request,
	and a tiny amount of javascript on the client (browser) for the sidebar. Everyone gets a fast experience!
	- Only executes anything when you want to update your site; run `./rendering/render.py`
* You really do get that nice, no-maintenance blog you always wanted.
* Written in Python, so it's even easy to install and run. *cough* jekyll *cough*

* Uses [solid software under the hood](#builton), so none of us (bloggers, readers, developers) have to reinvent the wheel.

Features
--------

* Works out a title for each article, to display in the `<title>` tag
* Uses a custom pandoc html template
* Article tags
    - uses the special `%tags:` line, containing a comma-seperated list of tags, which can contain spaces
    - generates an HTML page for each tag, listing all the articles with that tag
* Caches the last-rendered input (in lastinput/), so it knows what's changed since the last run
* An `%include` command, which includes the contents of another file (eg source code) in a given page
	- usage: `%include path/to/file.ext` on its own line. Files must have an extension, because otherwise they'd appear too dodgy for the internet
* Internal links between articles
* Syntax highlighting of `%include`d source code files
* Nicer anchor links support (less html-y, more pandocish) than standard markdown

###still to come:

* Date stamps, searching by date
* Authors support

<a name="builton"></a>Built Using
-----------

* [Pandoc](http://pandoc.org/) for the markdown-to-HTML rendering
* [PureCSS](http://purecss.io/) for the responsive stuff & sidebar
* Lots of regular expressions
* Some standard [GNU console programs](http://www.gnu.org/manual/blurbs.html) (diff, grep, head, tail, cat, echo, cp, mv...)
* Scripted using [Python](http://www.python.org/) 2
* That's all


Usage
---

Just upload/update your Markdown files in mdfiles/ (via SSH/rsync?), then run `rendering/render.py`

For more detail, read DOC.md

Requirements
----
* Pandoc 1.12+
* Python 2.7+


Longer Term:
------------
* what to put in sidebar?
	- About/Links (to my github, SO etc)
	- Other Blogs


%tags: readme
