if [ $# -eq 0 ]; then
    echo "no folder name provided"
    exit 1
fi
    
mkdir ../figure_save/$1
cp -r Test ../figure_save/$1
cp *.py ../figure_save/$1
cp *.sh ../figure_save/$1
cp *.pdf ../figure_save/$1



