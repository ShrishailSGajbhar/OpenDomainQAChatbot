import get_paragraphs
import get_most_relevant
import utils 
import bm25 
from get_paragraphs import Paragraphs
from get_most_relevant import RelevantParagraphExtracter
from utils import AnswerExtractor
from bm25 import BM25
import spacy
import os
from utils import QueryProcessor

class LongShortQAPipeline:
    def __init__(self, tokenizer, model) -> None:
        self.short_answer = None
        self.long_answer = None 
        self.short_extractor = AnswerExtractor(tokenizer, model)
    def get_all_short_answers(self, question, passages):
        short_answers = self.short_extractor.extract(question, passages)
        return short_answers

if __name__=='__main__':
    # query = "When did Satya Nadella become CEO of Microsoft?"
    # query = "when did russia invade ukraine?"
    
    query = input("Enter your query: \n")
    # print("\ninput query: ",query)
    SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
    nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
    query_processor = QueryProcessor(nlp)
    tokenized_query = query_processor.generate_query(query)
    print("\ntokenized query: ",tokenized_query)
    #------------------- paragraphs ------------------
    p = Paragraphs(query)
    print("query: ",p.query)
    print("\nTop-5 document URLs for the query: ",p.urls)
    #print(p.all_paras)
    print("\nTotal number of paragraphs are: {}".format(p.num_paras))
    #----------------------------------------------------
    extractor = RelevantParagraphExtracter(p.all_paras,10, nlp)
    passages = extractor.extract_most_relevant(query)
    print(f"\nTotal number of relevant paragraphs extracted are: {len(passages)}")

    #------- Short Answer extraction -------
    QA_MODEL = os.environ.get('QA_MODEL', 'deepset/roberta-base-squad2')
    extractor = LongShortQAPipeline(QA_MODEL, QA_MODEL)
    all_short_answers = extractor.get_all_short_answers(query,passages)
    print("\nTop 20 answers: ",all_short_answers)
    # Top short answer
    print("\ntop short answer: ",all_short_answers[0]['answer'])
    print("\ntop short answer score: ",all_short_answers[0]['score'])
    # Top long answer
    print("\ntop long answer: ",all_short_answers[0]['text'])

    






