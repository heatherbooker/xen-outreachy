from bs4 import BeautifulSoup
infile = open('index.html')
soup = BeautifulSoup(infile, 'html.parser')
outfile = open('mboxUrls.txt', 'w')

mboxes = soup.find_all('a')
for mbox in mboxes:
    link = mbox.get('href')
    if 'xen-devel' in link:
        outfile.write(link + '\n')

infile.close()
outfile.close()
