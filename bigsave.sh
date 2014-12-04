if [ $# -eq 0 ]; then
    echo "no folder name provided"
    exit 1
fi
    
mkdir ../bigsave/$1
cp -r Test ../bigsave/$1
cp *.py ../bigsave/$1
cp *.sh ../bigsave/$1
cp *.pdf ../bigsave/$1



