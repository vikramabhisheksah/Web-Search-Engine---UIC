import time
import config as cfg
from preprocess import Tokenizer
import utils
from page_rank import *
import pickle
from tfidf_ranker import *
'''
The script reads the local pages from the crawler, processes them, builds inverted index and
runs page rank, computes docs lengths, it then stores inverted index, page rank and docs length in a pickle file
'''

PAGE_RANK_MAX_ITER = cfg.params['page_rank_max_iter']
PAGE_COUNT = cfg.params['page_count']
FOLDER_NAME = cfg.params['folderName']
HOMEPAGE = cfg.params['homepage']
DOMAIN = utils.fetch_domain_name(HOMEPAGE)

start = time.time()

print('Started preprocessing '+str(PAGE_COUNT)+' pages')

tokenizer = Tokenizer(PAGE_COUNT,FOLDER_NAME,DOMAIN)
tokenizer.preprocess()
web_graph = tokenizer.web_graph
tokens = tokenizer.tokens

print(repr(web_graph))
prep = time.time()
print('Total preprocessing time:')
print(str(prep-start)+' seconds')
print('Running page rank')
page_rank = PageRank()
page_ranks = page_rank.page_rank(web_graph, PAGE_RANK_MAX_ITER)
print(page_ranks)

pr = time.time()
print('Total page rank running time:')
print(str(pr-prep)+' seconds')

inverted_index = tokenizer.inverted_index

print('Computing docs lengths')
tf_idf_ranker = TfidfRanker(inverted_index, PAGE_COUNT, page_ranks)
docs_length = tf_idf_ranker.compute_lengths(tokens)
inverted_index = tf_idf_ranker.inverted_index

with open('page_ranks_dict.pickle', 'wb') as handle:
    pickle.dump(page_ranks, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('inverted_index_dict.pickle', 'wb') as handle:
    pickle.dump(inverted_index, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('doc_lengths_dict.pickle', 'wb') as handle:
    pickle.dump(docs_length, handle, protocol=pickle.HIGHEST_PROTOCOL)

end = time.time()

print('total time:')
print(str(end-start)+' seconds')

