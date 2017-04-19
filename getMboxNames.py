import sys
from bs4 import BeautifulSoup
infile = open('index.html')
soup = BeautifulSoup(infile, 'html.parser')
outfile = open('mboxUrls.txt', 'w')

total_mboxes = 1 # Default: fetch 1.
try:
    if sys.argv[1] == 'all':
        total_mboxes = float('inf')
    else:
        total_mboxes = int(sys.argv[1])
except IndexError:
    pass
curr_mboxes = 0
mboxes = soup.find_all('a')
for mbox in mboxes:
    link = mbox.get('href')
    if 'xen-devel' in link:
        outfile.write(link + '\n')
        curr_mboxes += 1
        if curr_mboxes == total_mboxes:
            break

infile.close()
outfile.close()
