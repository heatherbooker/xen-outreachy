from perceval.backends.core.mbox import MBox
from elasticsearch import Elasticsearch
import hashlib
es = Elasticsearch()

src_url = 'https://lists.xenproject.org/archives/html/mbox/'
dest_dir = '/home/heather/dev/xen/sample'

repo = MBox(uri=src_url, dirpath=dest_dir)
logfile = open('mboxAnalysis.log', 'w')

def msg_to_bytes(msg):
    data = ''
    for key in msg:
        try:
            data += msg[key]
        except TypeError:
            pass
    return data.encode('utf-8')

def add_to_ES(doc_type, message, uuid):
        try:
            response = es.index(index="test", doc_type=doc_type, id=uuid, body=message)
        except UnicodeEncodeError as error:
            logfile.write('\n\nOh potatoes! Something broke: ' + str(error) + '\nCheck message with UUID: ' + uuid + ' to find the offending characters.')


prev_msg_hash = None
prev_uuid = None
for message in repo.fetch():
    try:
        refs = message['data']['References']
    except KeyError:
        pass # First msg in a thread doesn't have references.
    uuid = message['uuid']
    msg_in_bytes = msg_to_bytes(message['data'])
    msg_hash = hashlib.sha256(msg_in_bytes).hexdigest()
    if not prev_msg_hash == msg_hash and not uuid == prev_uuid:
        add_to_ES('message', message, uuid)
        prev_msg_hash = msg_hash
        prev_uuid = uuid

logfile.close()

