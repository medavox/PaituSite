#!/bin/bash
shopt -s extglob ##enable better bash regex support, ie for the ?(pattern) below

fileChanged=false
declare -A titles

function guaranteeFolder {
	if [ ! -d $1 ] ; then	
		mkdir $1
	fi
}

function checkFilesForUpdates {
	cd $1
	for f in *?(\ )*; do # allows bash to loop through files with spaces in their names
		g="${f// /_}" # replace spaces with underscores in filenames
		cleanedname=${g,,}
		dift=$(diff -qN "$f" ../lastinput/$cleanedname)
		if [ -n "$dift" ]; then # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
			#echo $f HAS CHANGED!
			guaranteeFolder ../temp # make sure temp directory exists
			fileChanged=true
			echo copying $f to ../temp/$cleanedname #make the name lowercase as well
			cp "$f" ../temp/"$cleanedname" # copy changed files to ../temp/ for rendering, in the next loop
			
			#add derived title to a bash associative array for use by pandoc later
			tytle=$(../rendering/getPageTitle.py "$f")
			titles[$cleanedname]="$tytle"
		fi
	done
	cd $OLDPWD
}

checkFilesForUpdates ../mdfiles

#todo: need to regenerate tags into bash dictionary once tagpage mdfiles have been generated
if $fileChanged ; then #if any files have changed, regenerate the tags
	../rendering/TagParser.py	#regenerate tag pages
fi

guaranteeFolder ../html # make sure html output directory exists
guaranteeFolder ../lastinput # make sure directory for saved copies of mdfiles last rendered exists

#render updated files in ../temp/ to html
cd ../temp
for x in *?(\ )* ; do
	echo rendering $x to ${x%md}html
	
	# extract a title from the doc first line, if the second line is r"===*"
	inDocTitle=$(head -n 2 "$x" | grep -B 1 "^=\{3,\}" | head -n 1)
	
	isTagPage=$(grep "Pages Tagged" "$x")
	if [ -z "$isTagPage" ] ; then
		title=${titles[$x]}
	else # (the tagpages didn't exist when the titles dictionary was populated in the last loop)
		
		title=$inDocTitle 
	fi
	echo title is "$title"
	
	if [ -n "$inDocTitle" ] ; then #if there's an in-document title, delete it from appearing in the document body
		inputFile=$(tail -n +3 "$x")
	else
		inputFile=$(cat "$x")
	fi
	
	#syntax highlighting example line
	#pygments needs the 'full' option in order to pass a stylesheet to the html doc
	#alternatively run pygments separately (with another argument set i don't know yet)
	#	to generate a standalone css file
	#don't forget that you can use `pygmentize -N` to guess a file's language based on its filename
	#pygmentize -l bash -f html -O linenos=inline,style=pastie,full -o ../render.sh.html render.sh 
	
	#RESULT=$(python -c 'import test; print test.get_foo()')
	
	#HERE is where we can do pre-processing before passing the resulting mdfile to pandoc
	inputFile="$(../rendering/finalPreprocessor.py "$(echo "$inputFile")" )"
	
	echo "$inputFile" | pandoc -M title="$title" -B ../rendering/tagEntries.html\
		-c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s\
		-r markdown+pipe_tables -w html -o ../html/${x%md}html
	#remember the pandoc --toc argument

	mv "$x" "../lastinput/$x"
done
