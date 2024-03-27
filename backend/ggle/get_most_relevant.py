'''
Module to get the topmost relevant paragraphs using BM25 from all the paragraphs.
'''
from .get_paragraphs import Paragraphs
from .bm25 import BM25
import spacy
import os
from .utils import QueryProcessor

class RelevantParagraphExtracter:
    def __init__(self, all_paragraphs, k, nlp) -> None:
        self.all_paras = all_paragraphs # it is list of paragraphs
        self.k = k # number of relevant paras to be extracted.
        self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
        self.bm25 = None

    def extract_most_relevant(self, question):
        corpus = [self.tokenize(p) for p in self.all_paras]
        self.bm25 = BM25(corpus)
        tokens = self.tokenize(question)
        scores = self.bm25.get_scores(tokens)
        pairs = [(s, i) for i, s in enumerate(scores)]
        pairs.sort(reverse=True)
        passages = [self.all_paras[i] for _, i in pairs[:self.k]]
        return passages
    
if __name__=='__main__':
    query = "When did Satya Nadella become CEO of Microsoft?"

    SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
    nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
    query_processor = QueryProcessor(nlp)
    tokenized_query = query_processor.generate_query(query)
    print(tokenized_query)
    #------------------- paragraphs ------------------
    p = Paragraphs(query)
    print("query: ",p.query)
    print("Top-5 document URLs for the query: ",p.urls)
    #print(p.all_paras)
    print("Total number of paragraphs are: {}".format(p.num_paras))
    #----------------------------------------------------
    extractor = RelevantParagraphExtracter(p.all_paras,3, nlp)
    passages = extractor.extract_most_relevant(query)
    print(f"Total number of relevant paragraphs extractd are: {len(passages)}")

    # for i in range(5):
    #     print(passages[i],"\n")
    reduce_text ='\n'.join([item for item in passages])
    # reduce_text ='\n\n'.join([item for item in passages])
    print(reduce_text)