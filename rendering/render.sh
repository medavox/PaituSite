#to do:
#keeping the .md version we rendered will help later with checking which files have changed and need re-rendering
# fix the fact that satripping out tags will mean the lastinput and mdffiles versions are always different

shopt -s extglob ##enable better bash regex support, ie for the ?(pattern) below
cd ../mdfiles
for f in *?(\ )*; do
	g="${f// /_}" # replace spaces with underscores in filenames
	dift=$(diff -qN "$f" ../lastinput/${g,,})
	if [ -n "$dift" ]; then # if working copy in ../mdfiles/ differs from last rendered version in ../lastinput/
		#echo $f HAS CHANGED!
		echo copying $f to ../temp/${g,,} #make the name lowercase as well
		cp "$f" ../temp/"${g,,}" # copy changed files to ../temp/ for rendering, in the next loop
		#cat "$f" | egrep -v ^%tags\{0,1\}:.*$ >> ../temp/"${g,,}"
	fi
done

#render updated files in ../temp/ to html
for x in $(ls ../temp) ; do
	echo rendering $x to ${x%md}html
	#work out a title
	title=$(head -n 2 "../temp/$x" | grep -B 1 "^=\{3,\}" | head -n 1) # extract a title from the doc first line, if the second line is ===*
	echo title is "$title"
	#head -n 3 mdfiles/ | egrep ^[a-zA-Z0-9 .,?!]{2,}$^=\{3,\}$ | grep -v ^=\{3,\}
	#head -n 2  | grep -v "^=\{3,\}"
	cat "../temp/$x" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -M title="$title" -B ../rendering/tagEntries.html\
		-c ../styles/style.css -c ../styles/side-menu.css --template=../rendering/template.html -s\
		-r markdown+pipe_tables -w html -o ../html/${x%md}html
	#cat ../rendering/header.html > ../html/${x%md}html
	#cat "../temp/$x" | egrep -v ^%tags\{0,1\}:.*$ | pandoc -c ../styles/style.css --toc -r markdown+pipe_tables -w html >> ../html/${x%md}html
	#cat ../rendering/footer.html >> ../html/${x%md}html
	mv ../temp/$x ../lastinput/$x
done