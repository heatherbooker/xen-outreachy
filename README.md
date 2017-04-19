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
python getMboxNames.py <number of mboxes you want to fetch> && ./getMboxes.sh
```

By default it will fetch one mbox. If you want more, specify the number as an argument to the python script. `all` will fetch all of the mboxes.

- Make sure ES is running (for me, this means `sudo systemctl start elasticsearch.service`).

- Analyze mbox data using Perceval, and input into Elasticsearch with each message thread being an ES "type":

__Warning:__ This may seriously tax your computer. Be wise.

```bash
python index_mbox.py
```

And now we wait, while it does its magic.

#### Querying:

```bash
python queries.py
```

More to come.

#### Caveats:

- Some messages appear to not get threaded. They are added under the type `unknown`.  
- My computer struggles as Elasticsearch attempts to consume all available resources and then some. Mileage may vary.

#### Improvements:

- Using the Elasticsearch [bulk API](https://elasticsearch-py.readthedocs.io/en/master/helpers.html#bulk-helpers) through the python script may reduce ingest time. That would be nice.  
- getMboxNames.py could randomly fetch archive names instead of sequentially.

BONUS:

Debugging is beautiful:

![Beautiful diagonal lines of alphanumeric characters in vim.](https://puu.sh/voZbF/1459719eee.pn://puu.sh/voZbF/1459719eee.png)

