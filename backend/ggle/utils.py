import itertools
#from rank_bm25 import BM25Okapi, BM25
from .bm25 import BM25
from multiprocessing import cpu_count
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline
import operator

class QueryProcessor:

    def __init__(self, nlp, keep=None):
        self.nlp = nlp
        self.keep = keep or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ'}

    def generate_query(self, text):
        doc = self.nlp(text)
        query = ' '.join(token.text for token in doc if token.pos_ in self.keep)
        return query

def effective_n_jobs(n_jobs):
    """Determines the number of jobs can run in parallel.

    Just like in sklearn, passing n_jobs=-1 means using all available
    CPU cores.

    Parameters
    ----------
    n_jobs : int
        Number of workers requested by caller.

    Returns
    -------
    int
        Number of effective jobs.

    """
    if n_jobs == 0:
        raise ValueError('n_jobs == 0 in Parallel has no meaning')
    elif n_jobs is None:
        return 1
    elif n_jobs < 0:
        n_jobs = max(cpu_count() + 1 + n_jobs, 1)
    return n_jobs

class AnswerExtractor:

    def __init__(self, tokenizer, model):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        model = AutoModelForQuestionAnswering.from_pretrained(model)
        self.nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)

    def extract(self, question, passages):
        answers = []
        for passage in passages:
            try:
                answer = self.nlp(question=question, context=passage)
                answer['text'] = passage
                answers.append(answer)
            except KeyError:
                pass
        answers.sort(key=operator.itemgetter('score'), reverse=True)
        return answers




