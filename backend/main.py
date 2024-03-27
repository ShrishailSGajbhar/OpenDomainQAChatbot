import os

import spacy
from flask import Flask, render_template, jsonify, request
from ggle.get_paragraphs import Paragraphs
from ggle.get_most_relevant import RelevantParagraphExtracter
from wiki.components import QueryProcessor, DocumentRetrieval, PassageRetrieval, AnswerExtractor

app = Flask(__name__)
SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
query_processor = QueryProcessor(nlp)
document_retriever = DocumentRetrieval()
passage_retriever = PassageRetrieval(nlp)
answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_wiki_answer', methods=['POST'])
def wiki_analyzer():
    data = request.get_json()
    question = data.get('question')

    query = query_processor.generate_query(question)
    docs = document_retriever.search(query)
    passage_retriever.fit(docs)
    passages = passage_retriever.most_similar(question)
    answers = answer_extractor.extract(question, passages)
    return jsonify(answers)


@app.route('/get_google_answer', methods=['POST'])
def google_analyzer():
    data = request.get_json()
    question = data.get('question')
    query = query_processor.generate_query(question)
    p = Paragraphs(query)
    extractor = RelevantParagraphExtracter(p.all_paras,20, nlp)
    passages = extractor.extract_most_relevant(question)
    answers = answer_extractor.extract(question, passages)
    print(answers)
    return jsonify(answers)

if __name__ == '__main__':
    app.run()
