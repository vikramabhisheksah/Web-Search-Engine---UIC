from os import stat
from ExtractLinks import ExtractLinks
from utils import *
import urllib.request as urllib
import pickle

class Crawl:
    thread_count = 0
    queue = set()
    crawled = set()
    file_from_url = {}
    url_from_file = {}
    def __init__(self, folder,page_url,domain):
        Crawl.folder = folder
        Crawl.webpage_folder = Crawl.folder + "/webpages/"
        Crawl.page_url = page_url
        Crawl.domain = domain
        self.initial_setup()
        self.crawl_page(Crawl.page_url)

    @staticmethod
    def initial_setup():
        create_directory(Crawl.folder)
        create_directory(Crawl.webpage_folder)
        Crawl.queue.add(Crawl.page_url)

    @staticmethod
    def crawl_page(page_url):
        if page_url not in Crawl.crawled:
            print('crawling ' + page_url)
            print('Queue ' + str(len(Crawl.queue)) + ', Crawled  ' + str(len(Crawl.crawled)))
            all_links = Crawl.get_links_from_page(page_url)
            Crawl.add_to_queue(all_links)
            Crawl.queue.remove(page_url)
            Crawl.crawled.add(page_url)
            write_set_to_file(Crawl.crawled,Crawl.folder+ "/crawled_links")
        
    @staticmethod
    def get_links_from_page(page_url):
        try:
            html_page = urllib.urlopen(page_url,timeout=10)
            if 'text/html' in html_page.getheader('Content-Type'):
                html_string = html_page.read().decode("utf-8")
                count = Crawl.thread_count
                Crawl.thread_count+=1

                write_to_file(Crawl.webpage_folder + str(count),html_string)
                links = ExtractLinks(page_url,Crawl.domain, True)
                links.feed(html_string)
                all_links = links.get_links()

                Crawl.file_from_url[page_url] = count
                Crawl.url_from_file[count] = page_url
                if count % 1000 == 0:
                    print('save file_from_url and url_from_file as pickle files in binary')
                    with open('file_from_url_dict.pickle', 'wb') as handle:
                        pickle.dump(Crawl.file_from_url, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    with open('url_from_file_dict.pickle', 'wb') as handle:
                        pickle.dump(Crawl.url_from_file, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            return set()
        return all_links
    
    @staticmethod
    def add_to_queue(links):
        for url in links:
            if (url in Crawl.queue) or (url in Crawl.crawled):
                continue
            Crawl.queue.add(url)