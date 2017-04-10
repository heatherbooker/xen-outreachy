## Xen Outreachy Microtask

#### Objective: 

- Use Perceval to analyze Xen's xen-devel mailing lists and Git history.
- Store resulting info in Elasticsearch.
- Determine branch associated with Git commits, and add this info to Elasticsearch.


#### Setup:

```bash
git clone https://github.com/heatherbooker/xen-outreachy.git
cd xen-outreachy
mkvirtualenv -p <path/to/python3.4+> xen-outreachy  # Or use virtualenv if preferred.
pip install -r requirements.txt
```
Also install Elasticsearch.

#### Steps:

- Download list of mailing list archives:

```bash
wget https://lists.xenproject.org/archives/html/mbox/
```

- Download xen-devel mboxes only (__if using bash shell, modify first line of getMboxes.sh first!__):

```bash
python getMboxNames.py
./getMboxes.sh
```

- Analyze mbox data using Perceval, and input into Elasticsearch:

```bash
python perceval-mbox.py
```

- Get Git data, analyze using Perceval, and input into Elasticsearch ([thanks Grimoirelab training!](https://jgbarah.gitbooks.io/grimoirelab-training/grimoireelk/a-simple-dashboard.html)):

```bash
# Enter all three lines together! Not three separate commands! :)
p2o.py --enrich --index git_raw --index-enrich git \
-e http://localhost:9200 --no_inc --debug \
git https://xenbits.xen.org/git-http/xen.git
```

TBC...
