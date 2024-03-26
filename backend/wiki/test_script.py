import os

import spacy

from components import QueryProcessor, DocumentRetrieval, PassageRetrieval, AnswerExtractor

question = "When did Satya Nadella became CEO of Microsoft"

SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
query_processor = QueryProcessor(nlp)
document_retriever = DocumentRetrieval()
passage_retriever = PassageRetrieval(nlp)
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)



query = query_processor.generate_query(question)
docs = document_retriever.search(query)
passage_retriever.fit(docs)
passages = passage_retriever.most_similar(question)
answers = answer_extractor.extract(question, passages)

print(answers)