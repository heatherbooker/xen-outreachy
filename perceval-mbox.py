from perceval.backends.core.mbox import MBox
from elasticsearch import Elasticsearch
es = Elasticsearch()

src_url = 'https://lists.xenproject.org/archives/html/mbox/'
dest_dir = '/home/heather/dev/xen/sample'

repo = MBox(uri=src_url, dirpath=dest_dir)
logfile = open('mboxAnalysis.log', 'w')

for message in repo.fetch():
    try:
        response = es.index(index="test", doc_type="message", id=message['uuid'], body=message)
    except UnicodeEncodeError as error:
        logfile.write('\n\nOh potatoes! Something broke: ' + str(error) + '\nCheck message with UUID: ' + message['uuid'] + ' to find the offending characters.')

logfile.close()

