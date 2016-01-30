TODO
----

* Nicer anchor links support (less html-y, more pandocish) than standard markdown
* Reimplement generation of a page listing all tags, and also untagged pages
* add warning when tagpage overwrites existing file (article?)
* create new `.list` file format, where each line is a bullet point
	- titles are either a line surrounded by blank lines (or the beginning of the file),
	- or the first item in a list of lines
	- indentation of lists can work with tabs/spaces of lines
* In rendered page, put labelled box around `%include`d code, with a download link (the filename)
	- also insert language next to markdown code fence, if detectable
* fix the fact that stripping out tags will mean the lastinput and mdfiles versions are always different
* Date page written, and/or date last updated
* Multiple Author support?
* put generated tag pages in their own directory?


DONE
----
* The tags (if any) a page has are added as a list of links to the bottom of that page
* Clickable list of articles with a given tag
* special `%include` directive, to include the contents of a file inside the rendered copy of another


something weird with the diffing
generate all_tags page and untagged_articles
