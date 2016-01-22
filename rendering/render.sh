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
	
	isTagPage=$(grep "Pages Tagged" "$x")
	tagfooter=""
	if [ -z "$isTagPage" ] ; then #only add its tag list to this page, if it isn't itself a tag page
		../rendering/getTags.py "$x"
		tagfooter="-A ../tagfooter.txt"
		title=${titles[$x]}
	else # (the tagpages didn't exist when the titles dictionary was populated in the last loop)
		inDocTitle=$(head -n 2 "$x" | grep -B 1 "^=\{3,\}" | head -n 1)
		title=$inDocTitle 
	fi
	
	# extract a title from the doc first line, if the second line is r"===*"
	echo title is "$title"
	
	if [ -n "$inDocTitle" ] ; then #if there's an in-document title, delete it from appearing in the document body
		inputFile=$(tail -n +3 "$x")
	else
		inputFile=$(cat "$x")
	fi
	
	#HERE is where we can do the final pre-processing before passing the resulting mdfile to pandoc
	#sed "s_(\[.+\]\()((?!http://)[^/])\)_\1\2.html\)_g")
	inputFile="$(../rendering/finalPreprocessor.py "$(echo "$inputFile")" )"
	
	echo "$inputFile" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -M title="$title" -B ../rendering/tagEntries.html\
		-c ../style/style.css -c ../style/side-menu.css --template=../rendering/template.html -s\
		-r markdown+pipe_tables -w html $tagfooter -o ../html/${x%md}html
	#--toc
	#cat ../rendering/footer.html >> ../html/${x%md}html

	mv "$x" "../lastinput/$x"
done

rm ../tagfooter.txt
