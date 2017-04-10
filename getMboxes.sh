#!/usr/bin/zsh

MBOX_URLS='mboxUrls.txt'
ENDPOINT="https://lists.xenproject.org/archives/html/mbox/"
DIR='mboxes/'
EXT=".txt"

# Each line of MBOX_URLS file is an mbox filename.
while read -r filename
do
    mbox=$ENDPOINT$filename
    content="$(curl -s $mbox)"
    echo "$content" >> $DIR$filename$EXT
done < "$MBOX_URLS"

echo "Retrieved mboxes"

