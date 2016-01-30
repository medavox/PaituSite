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
* An `%include` command, which includes the contents of another file (eg source code) in a given page
	- usage: `%include path/to/file.ext` on its own line. Files must have an extension, because otherwise they'd appear too dodgy for the internet
* Link between different pages on blog
* Syntax highlighting of `%include`d source code files
* Nicer anchor links support (less html-y, more pandocish) than standard markdown

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
* what to put in sidebar?
	- Tag List
	- About/Links (to my github, SO etc)
	- Other Blogs


%tags: readme
