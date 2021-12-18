from preprocess import Tokenizer
from tfidf_ranker import TfidfRanker
import pickle
import config as cfg
import utils
'''
This script is the main program of this project, by running it the user is displayed a prompt where he can 
enter his queries and see the results
'''

PAGE_COUNT = cfg.params['page_count']
FOLDER_NAME = cfg.params['folderName']
HOMEPAGE = cfg.params['homepage']
DOMAIN = utils.fetch_domain_name(HOMEPAGE)

RESULTS_PER_PAGE = 10
MAX_RESULTS_TO_CONSIDER = 50


def load_files():
    #Loading all the necessary files to run the queries and return ranked urls

    global url_from_file, file_from_url, inverted_index, docs_length, page_ranks, docs_tokens

    with open('url_from_file_dict.pickle', 'rb') as handle:
        url_from_file = pickle.load(handle)
    with open('file_from_url_dict.pickle', 'rb') as handle:
        file_from_url = pickle.load(handle)
    with open('inverted_index_dict.pickle', 'rb') as handle:
        inverted_index = pickle.load(handle)
    with open('doc_lengths_dict.pickle', 'rb') as handle:
        docs_length = pickle.load(handle)
    with open('page_ranks_dict.pickle', 'rb') as handle:
        page_ranks = pickle.load(handle)
    with open('docs_tokens_dict.pickle', 'rb') as handle:
        docs_tokens = pickle.load(handle)


def new_query(query):
    query_tokens = tokenizer.tokenization(query)
    best_ranked = tf_idf_ranker.retrieve_most_relevant(query_tokens)[:MAX_RESULTS_TO_CONSIDER]
    handle_show_query(best_ranked, RESULTS_PER_PAGE)

def handle_show_query(best_ranked, n):
    print('Here are the results \n')
    url_list = [str(url_from_file[count[0]])+' '+str(count[1]) for count in best_ranked[:n]]
    url_list.append("Enter 1 to show more results, 2 to exit")

    for link in url_list:
        print(link,"\n")
    
    choice = str(input("Enter 1 to show more results, 2 to start again, 3 to exit "))
    if choice == '1':
        handle_show_query(best_ranked, n + RESULTS_PER_PAGE)
    elif choice =='2':
        start_engine()
    else:
        return
    

def start_engine():
    global tokenizer, tf_idf_ranker

    load_files()
    tokenizer = Tokenizer(PAGE_COUNT,FOLDER_NAME, DOMAIN)
    tf_idf_ranker = TfidfRanker(inverted_index, PAGE_COUNT, page_ranks, docs_length, True)

    print('\n                     ---UIC Web Search Engine---\n')
    query = str(input("Enter a search query: "))
    print('\n')
    new_query(query)

start_engine()

