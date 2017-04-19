from perceval.backends.core.mbox import MBox
from elasticsearch import Elasticsearch
import hashlib
from jwzthreading import thread, Message
es = Elasticsearch()

src_url = 'https://lists.xenproject.org/archives/html/mbox/'
dest_dir = '/home/heather/dev/xen/sample'

repo = MBox(uri=src_url, dirpath=dest_dir)
logfile = open('mboxAnalysis.log', 'w')

def log_error(error, uuid=None, is_message=False):
    err_log = '\nOh potatoes! Something broke: ' + str(error)
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


def parse_messages(repo):
    original_msg_count = 0
    message_list = []
    message_map = {}
    prev_msg_hash = None
    prev_uuid = None
    counter = 0
    for message in repo.fetch():
        original_msg_count += 1
        uuid = message['uuid']
        msg_in_bytes = msg_to_bytes(message['data'])
        msg_hash = hashlib.sha256(msg_in_bytes).hexdigest()
        if not prev_msg_hash == msg_hash and not uuid == prev_uuid:
            counter += 1
            message_list.append(get_jwz_message(message, uuid))
            prev_msg_hash = msg_hash
            prev_uuid = uuid
            message_map[uuid] = message
    print('Total unique messages: ' + str(counter))
    print('Original messages fetched from mbox: ' + str(original_msg_count))
    return message_list, message_map

def collect_msg_ids(container):
    yield container['id']
    for child in container['children']:
        yield from collect_msg_ids(child)

def get_es_type(container):
    root_message = message_map[container['id']]
    thread_subject = root_message['data']['Subject']
    return ''.join(c for c in thread_subject if (c.isalnum() or c.isspace()))

def index_thread_in_ES(ctr, ischild):
    container = None
    try:
        container = ctr.to_dict()
        es_type = get_es_type(container)
        for msg_id in collect_msg_ids(container):
            # Pop removes and retrieves msg.
            add_to_ES('message', message_map.pop(msg_id))
    except ValueError as error:
        log_error(error)
        for child_ctr in ctr.children:
            index_thread_in_ES(child_ctr, True)


message_list, message_map = parse_messages(repo)
containers = thread(message_list, group_by_subject=False)

for ctr in containers:
    index_thread_in_ES(ctr, False)

logfile.write('\n\nRemaining messages that have not been added to ES: ' + str(message_map.keys()))

logfile.close()

