from perceval.backends.core.mbox import MBox
from elasticsearch import Elasticsearch
import hashlib
from jwzthreading import thread, Message
es = Elasticsearch()

src_url = 'https://lists.xenproject.org/archives/html/mbox/'
dest_dir = '/home/heather/dev/xen/sample'

repo = MBox(uri=src_url, dirpath=dest_dir)
logfile = open('mboxAnalysis.log', 'w')

def log_error(error, uuid, is_message):
    err_log = '\n\nOh potatoes! Something broke: ' + str(error)
    if is_message:
        err_log += '\nCheck message with UUID:' + uuid
    logfile.write(err_log)

def msg_to_bytes(msg):
    data = ''
    for key in msg:
        try:
            data += msg[key]
        except TypeError:
            pass
    return data.encode('utf-8')

def get_jwz_message(message, uuid):
    jwz_msg = Message(msg=message['data'], message_idx=uuid)
    return jwz_msg

def add_to_ES(doc_type, message):
    try:
        response = es.index(index="test", doc_type=doc_type,
                id=message['uuid'], body=message)
    except UnicodeEncodeError as error:
        log_error(error, message['uuid'], True)        


message_map = {}
def parse_messages(repo):
    message_list = []
    prev_msg_hash = None
    prev_uuid = None
    for message in repo.fetch():
        uuid = message['uuid']
        msg_in_bytes = msg_to_bytes(message['data'])
        msg_hash = hashlib.sha256(msg_in_bytes).hexdigest()
        if not prev_msg_hash == msg_hash and not uuid == prev_uuid:
            message_list.append(get_jwz_message(message, uuid))
            prev_msg_hash = msg_hash
            prev_uuid = uuid
            message_map[uuid] = message
    return message_list

message_list = parse_messages(repo)
containers = thread(message_list, group_by_subject=False)

for ctr in containers:
    try:
        container = ctr.to_dict()
        root_message = message_map[container['id']]
        thread_subject = root_message['data']['Subject']
        es_type = ''.join(c for c in thread_subject if (c.isalnum() or c.isspace()))
        add_to_ES(es_type, root_message)
    except ValueError as error:
        log_error(error, str(ctr), False)

logfile.close()

