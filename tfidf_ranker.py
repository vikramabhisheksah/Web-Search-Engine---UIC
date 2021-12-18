import math
from collections import Counter
import operator

def rank_docs(similarities):
    #Orders a dict of similarities based on similarity value
    return sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)

class TfidfRanker:

    PAGE_RANK_MULTIPLIER = 20

    def __init__(self, inverted_index, page_count, page_ranks, docs_length={}, idf_calculated_already=False):
        self.inverted_index = inverted_index
        self.page_count = page_count
        self.page_ranks = page_ranks
        self.idf = self.compute_idf()
        self.doc_length = docs_length
        if not idf_calculated_already:
            self.compute_all_tf_idf()

    
    def tf_idf(self, word, doc):
        # saving tfidf into inverted index
        self.inverted_index[word][doc] = self.inverted_index[word][doc] * self.idf[word]
        return self.inverted_index[word][doc]

    def compute_idf(self):
        df = {}
        idf = {}
        for key in self.inverted_index.keys():
            df[key] = len(self.inverted_index[key].keys())
            idf[key] = math.log(self.page_count / df[key], 2)
        return idf
    
    def compute_all_tf_idf(self):
        for word in self.inverted_index:
            for doc_key in self.inverted_index[word]:
                self.tf_idf(word, doc_key)

    def compute_doc_length(self, file_count, tokens):
        bag_of_words = []
        length = 0
        for token in tokens:
            if token not in bag_of_words:
                length += self.tf_idf(token, file_count) ** 2
                bag_of_words.append(token)
        return math.sqrt(length)
    
    def compute_lengths(self, tokens):
        for file_count in range(self.page_count):
            self.doc_length[file_count] = self.compute_doc_length(file_count, tokens[file_count])
        return self.doc_length

    def inner_product_similarities(self, query_tokens):
        similarity = {}
        for word in query_tokens:
            wq = self.idf.get(word,0)
            if wq != 0:
                for doc in self.inverted_index[word].keys():
                    similarity[doc] = similarity.get(doc, 0) + self.inverted_index[word][doc] * wq
        return similarity

    def query_length(self, query_tokens):
        # no query has repeated words
        length = 0
        cnt = Counter()
        for w in query_tokens:
            cnt[w] += 1
        for w in cnt.keys():
            length += (cnt[w]*self.idf.get(w, 0)) ** 2
        return math.sqrt(length)

    def cosine_similarities(self, query_tokens):
        similarity = self.inner_product_similarities(query_tokens)
        for doc in similarity.keys():
            similarity[doc] = (similarity[doc] / self.doc_length[doc])/ self.query_length(query_tokens)
        return similarity

    def cosine_page_rank(self, query_tokens):
        cosine_similarity = self.cosine_similarities(query_tokens)
        cosine_page_rank_sim = {key: cosine_similarity[key]+self.page_ranks[key]*TfidfRanker.PAGE_RANK_MULTIPLIER
                                for key in cosine_similarity}
        return cosine_page_rank_sim

    #Returns list of tuples (doc_code, similarity) in descending order of similarity
    def retrieve_most_relevant(self, query_tokens):
        return rank_docs(self.cosine_page_rank(query_tokens))
    



