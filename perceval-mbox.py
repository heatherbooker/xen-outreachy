from perceval.backends.core.mbox import MBox
from elasticsearch import Elasticsearch
es = Elasticsearch()

src_url = 'https://lists.xenproject.org/archives/html/mbox/'
dest_dir = '/home/heather/dev/xen/mboxsample'

repo = MBox(uri=src_url, dirpath=dest_dir)
logfile = open('mbox-perceval-analysis.log', 'w')

nextMessageId = 0
for message in repo.fetch():
    nextMessageId += 1
    try:
        response = es.index(index="test", doc_type="message", id=nextMessageId, body=message)
    except UnicodeEncodeError as e:
        logfile.write('oh potatoes! something broke: ' + str(e))
        encodedbody = message['data']['body']['plain'].encode('iso-8859-1', 'ignore')
        message['data']['body']['plain'] = str(encodedbody)
        response = es.index(index='test', doc_type="message", id=nextMessageId, body=message)
        logfile.write('\nwe tried again. check id' + str(nextMessageId) + ' for details.\n\n')
    if not response['created']:
        logfile.write(str(response) + '\n\n')

logfile.close()

