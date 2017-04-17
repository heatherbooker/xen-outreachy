## Xen Outreachy Microtask

#### Objective: 

- Use Perceval to analyze Xen's xen-devel mailing lists.
- Store resulting info in Elasticsearch, with messages labeled by thread.


#### Setup:

```bash
git clone https://github.com/heatherbooker/xen-outreachy.git
cd xen-outreachy
mkvirtualenv -p <path/to/python3.4+> xen-outreachy  # Or use virtualenv if preferred.
pip install -r requirements.txt
```
You also need to have Elasticsearch installed.

#### Steps:

- Download list of mailing list archives:

```bash
wget https://lists.xenproject.org/archives/html/mbox/
```

- Download xen-devel mboxes (__if using bash shell, modify first line of getMboxes.sh first!__):

```bash
python getMboxNames.py
./getMboxes.sh
```

- Make sure ES is running (for me, this means `sudo systemctl start elasticsearch.service`).

- Analyze mbox data using Perceval, and input into Elasticsearch with each message thread being an ES "type":

```bash
python perceval-mbox.py
```

