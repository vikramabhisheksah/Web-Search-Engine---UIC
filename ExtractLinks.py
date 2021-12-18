from html.parser import HTMLParser
from urllib import parse
from utils import *

class ExtractLinks(HTMLParser):

    def __init__(self, page_url,  domain, restrict=True,):
        super().__init__()
        self.page_url = page_url
        self.restrict = restrict
        self.domain = domain
        self.blocklist = (".doc", ".docx",  ".avi", ".mp4", ".jpg", ".jpeg", ".png", ".gif", ".pdf",
                        ".gz", ".rar", ".tar", ".tgz", ".zip", ".exe", ".js", ".css", ".ppt", ".pptx", ".mov")
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (att, val) in attrs:
                if att == 'href':
                    complete_url = parse.urljoin(self.page_url, val)
                    if not complete_url.lower().endswith(self.blocklist):
                        complete_url = complete_url.strip()
                        complete_url = complete_url.rstrip('/')
                        complete_url = complete_url.split('#')[0]
                        complete_url = complete_url.split('<')[0]
                        complete_url = complete_url.split('?', maxsplit=1)[0]
                        x = complete_url.split(':')
                        if x[0] == 'http' and len(x)==2:
                            complete_url = x[0]+'s:'+x[1]
                        if complete_url and self.restrict and fetch_domain_name(complete_url)==self.domain:
                                self.links.add(complete_url)
                        
    def get_links(self):
        return self.links
