from perceval.backends.core.git import Git

src_url = 'https://github.com/heatherbooker/graphmarks.git'
dest_dir = '~/dev/graphmarks'

repo = Git(uri=src_url, gitpath=dest_dir)

heathers = 0
denizs = 0
for commit in repo.fetch():
    author = commit['data']['Author']
    if "Heather" in author:
        heathers += 1
    else:
        denizs += 1
print('heathers: ' + str(heathers) + ', denizes: ' + str(denizs))

