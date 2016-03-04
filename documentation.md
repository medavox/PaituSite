How To Use Ysgrifen
=====


This document will show you how to use the various features Ysgrifen provides.

Markdown Flavour
------

Ysgrifen's flavour of Markdown is defined by Pandoc as:-

```
markdown
+pipe_tables
+autolink_bare_uris
+inline_notes
```

This is defined at [line ~177 of render.py](https://github.com/medavox/Ysgrifen/blob/master/rendering/render.py#L177),
so if you want to add or remove markdown extensions, do it there.

Basic Usage
------

In the project root directory (with the `README.md` in it):

1. Create a directory named `articles`
2. Write some Markdown, save it in `articles` with the .md extension
3. run `./rendering/render.py`
  - or `python rendering/render.py` if you're not using Linux
5. Point your webserver's root directory to `html/`. This is where your generated site lives!



Tags
----

Tags are added a document by comma-separating them on one line, which must begin with `%tag:` or `%tags:`, like so:-

```

<article text blah bah...>

%tags:food,things that are red, el_chupacabra

```

Notice that tags can contain spaces. Spaces before or after commas asre also ignored.
For obvious reasons, tags can't contains commas, dummy.


Including Files
------

Ysgrifen allows you to include the contents of another file in your document at render-time,
as if you had copy-pasted it in there.

Just do `%include <filename.ext>` on its own line; Ysgrifen will look for the file in the `./includes` folder.

This is useful for including source code in a document; just don't forget to wrap the `%include`
statement in a Markdown code-fence:

<code>
```python

%include awesome_source.py

```
</code>

Linking to Other Articles
