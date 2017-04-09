#!/usr/bin/zsh

NUM_SCRIPTS=5
ENDPOINT="https://lists.xenproject.org/archives/html/mbox/"
FILE="xen-devel-2015-0"
EXT=".txt"


for i in {1..$NUM_SCRIPTS}
do
    filename=$FILE$i
    mbox=$ENDPOINT$filename
    content="$(curl -s $mbox)"
    echo "$content" >> $filename$EXT 
done

echo "Retrieved $NUM_SCRIPTS mboxes"

