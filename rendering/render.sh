#!/bin/bash
#to do:
#keeping the .md version we rendered will help later with checking which files have changed and need re-rendering
# fix the fact that satripping out tags will mean the lastinput and mdffiles versions are always different
shopt -s extglob ##enable better bash regex support, ie for the ?(pattern) below
cd ../mdfiles
fileChanged=false
declare -A titles
for f in *?(\ )*; do # allows bash to loop through files with spaces in their names
	g="${f// /_}" # replace spaces with underscores in filenames
	cleanedname=${g,,}
	dift=$(diff -qN "$f" ../lastinput/$cleanedname)
	if [ -n "$dift" ]; then # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
		#echo $f HAS CHANGED!
		if [ ! -d ../temp ] ; then # make sure temp directory exists
			mkdir ../temp
		fi
		fileChanged=true
		echo copying $f to ../temp/$cleanedname #make the name lowercase as well
		cp "$f" ../temp/"$cleanedname" # copy changed files to ../temp/ for rendering, in the next loop
		#cat "$f" | egrep -v ^%tags\{0,1\}:.*$ >> ../temp/"${g,,}"
		tytle=$(python ../rendering/getPageTitle.py "$f")
		titles[$cleanedname]=$tytle
		#echo "%title:$tytle" >> ../temp/$cleanedname
	fi
done

if $fileChanged ; then #if any files have changed, regenerate the tags and sidemenu
	../rendering/TagParser.py
fi

#todo: call the getTitle() python function somehow (put it in its own file?)

#render updated files in ../temp/ to html
for x in $(ls ../temp) ; do
	echo rendering $x to ${x%md}html
	#work out a title
	inDocTitle=$(head -n 2 "../temp/$x" | grep -B 1 "^=\{3,\}" | head -n 1) # extract a title from the doc first line, if the second line is r"===*"
	title=${titles[$x]}
	echo title is "$title"
	#head -n 3 mdfiles/ | egrep ^[a-zA-Z0-9 .,?!]{2,}$^=\{3,\}$ | grep -v ^=\{3,\}
	#head -n 2  | grep -v "^=\{3,\}"
	if [ ! -d ../html ] ; then	# make sure html output directory exists
		mkdir ../html
	fi
	
	if [ -n "$inDocTitle" ] ; then #if there's an in-document title, delete it from appearing in the document body
		tail -n +3 "../temp/$x" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -M title="$title" -B ../rendering/tagEntries.html\
		-c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s\
		-r markdown+pipe_tables -w html -o ../html/${x%md}html
	else
		cat "../temp/$x" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -M title="$title" -B ../rendering/tagEntries.html\
		-c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s\
		-r markdown+pipe_tables -w html -o ../html/${x%md}html
	fi
	#cat ../rendering/header.html > ../html/${x%md}html
	#cat "../temp/$x" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -c ../styles/style.css --toc -r markdown+pipe_tables -w html >> ../html/${x%md}html
	#cat ../rendering/footer.html >> ../html/${x%md}html
	if [ ! -d ../lastinput ] ; then
		mkdir ../lastinput
	fi
	mv ../temp/$x ../lastinput/$x
done
