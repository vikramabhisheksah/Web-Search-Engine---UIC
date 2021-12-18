#vikram sah
import os
from urllib import parse

def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def create_directory(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

def fetch_domain_name(url):
    try:
        results = parse.urlparse(url).netloc.split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

def write_set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")