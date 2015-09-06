```
for each .md file:
	if there's a line which begins with %tag:
		ignore an s if there is one
		from the colon, parse the words, splitting by comma (and removing any spaces), in a list of tags
```	
from this, you can derive:
* a total list of all tags occurring across all files
* a list of files which have each of the tags
