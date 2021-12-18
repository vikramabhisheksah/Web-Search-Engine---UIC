from selectolax.parser import HTMLParser
from ExtractLinks import ExtractLinks
from utils import *
import re
import string
import graph
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

class Tokenizer:

    web_graph = graph.OptimizedDirectedGraph()
    file_from_url = {}
    with open('file_from_url_dict.pickle', 'rb') as handle:
        file_from_url = pickle.load(handle)

    def __init__(self, page_count, folder, domain):
        self.FOLDER = folder
        self.page_count = page_count
        self.domain = domain
        self.stop_words = set(stopwords.words('english'))
        self.inverted_index = {}
        self.stemmer = PorterStemmer()
        self.tokens = {}

    @staticmethod
    def get_text_selectolax(html):
        tree = HTMLParser(html)
        if tree.body is None:
            return None
        for tag in tree.css('script'):
            tag.decompose()
        for tag in tree.css('style'):
            tag.decompose()
        text = tree.body.text(separator=' ')
        return text

    def preprocess(self):
        for file_count in range(self.page_count):
            with open(self.FOLDER + '/webpages/' + str(file_count)) as f:
                file_text = f.read()
            if file_text is not None:
                self.get_text_from_page(int(file_count), file_text)

            extract_links = ExtractLinks(self.FOLDER, self.domain, True)
            extract_links.feed(file_text)
            links = extract_links.get_links()
            Tokenizer.web_graph.add_node(file_count)
            for out_link in links:
                if out_link in Tokenizer.file_from_url:
                    Tokenizer.web_graph.add_edge(file_count,Tokenizer.file_from_url[out_link])

    def get_text_from_page(self, file_count, file_text):
        file_text = self.get_text_selectolax(file_text)
        if file_text is None:
            file_text = 'blank'
        self.tokens[file_count] = self.tokenization(file_text)
        self.add_to_inverted_index(file_count, self.tokens[file_count])

    def add_to_inverted_index(self, count, tokens):
        for token in tokens:
            self.inverted_index.setdefault(token, {})[count] = self.inverted_index.setdefault(token, {}).get(count, 0) + 1

    def tokenization(self, file_text):
        tokens = file_text.split()
        tokens = [''.join(c for c in t if c not in string.punctuation) for t in tokens]
        tokens = [t.lower() for t in tokens]
        tokens = map(remove_numbers, tokens)
        tokens = map(self.stemmer.stem, tokens)
        tokens = [t for t in tokens if not less_than_two_letters(t)]
        # stop words elimination
        tokens = [t for t in tokens if t not in self.stop_words]
        tokens = [t for t in tokens if t]
        return tokens

def remove_numbers(st):
    return re.sub('\d', '', st)

# returns true if the word has less or equal 2 letters
def less_than_two_letters(word):
    return len(word) <= 2






