#to do:
#add functionality to check whether lastinput version is the same as mdfiles version, and only overwrite and re-render with the (obviously newer) mdfiles version if they're different

#create copies of .md files with space in filenames removed
#keeping the .md version we rendered will help later with checking which files have changed and need re-rendering
for f in ../mdfiles/*\ *; do
	cp ../mdfiles/"$f" ../lastinput/"${f// /_}"
done

#render the de-space-named files to html
for x in $(ls ../lastinput) ; do
	echo rendering $x to ${x%md}html
	pandoc -c ../styles/style.css --toc -s -r markdown+pipe_tables -w html -o ../html/${x%md}htm ../lastinput/$x
done
