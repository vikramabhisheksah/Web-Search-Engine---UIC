import threading
from crawler import Crawl
from utils import *
from queue import Queue
import config as cfg

folder = cfg.params['folderName']
homepage = cfg.params['homepage']
threads = cfg.params['threads']

domain = fetch_domain_name(homepage)
qu = Queue()
Crawl(folder,homepage,domain)


def begin_crawl():
     create_workers()
     while True:
         add_job_to_queue()


def create_workers():
    for _ in range(threads):
        t = threading.Thread(target=task, daemon=True)
        t.start()

def task():
    while True:
        link = qu.get()
        print("Thread deployed ", threading.current_thread().name)
        Crawl.crawl_page(link)
        qu.task_done()

def add_job_to_queue():
    try:
        for link in Crawl.queue:
            qu.put(link)
        qu.join()
    except:
        print(Crawl.queue)
begin_crawl()