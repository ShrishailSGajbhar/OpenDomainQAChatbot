import requests
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup

class Paragraphs:
    def __init__(self, query, num_docs=10):
        self.query = query # input query
        self.num_docs = num_docs # num of docs to be retrieved
        self.urls = self.get_urls()
        self.all_paras = self.get_all_paragraphs() # list containing all paragraphs
        self.num_paras=len(self.all_paras) # shows total number of paragraphs

    def get_urls(self):
        '''
        This function fetches the top(#num_docs) documents for the given query
        '''
        url_list = list(search(self.query, tld="co.in", num=10, stop=self.num_docs, pause=2))
        # These above urls may contain media so filtering them out
        final_links=[]
        with requests.Session() as session:
            for link in url_list:
                if "text/html" in session.head(link).headers.get("content-type",""):
                    final_links.append(link)
        return final_links
    def get_all_paragraphs(self):
        all_paras = []
        for url in self.get_urls():
            page = requests.get(url)
            tree = html.fromstring(page.content)
            soup = BeautifulSoup(page.content, features="lxml")
            article_text = ''
            article = soup.findAll('p')
            for element in article:
                article_text += '\n' + ''.join(element.findAll(text = True))
            article_paras = article_text.split('\n')
            all_paras.extend(article_paras)
        return all_paras


if __name__=='__main__':
    # query = "When did Satya Nadella become CEO of Microsoft?"
    query = "Where on Earth is free exygen found?"
    p = Paragraphs(query)
    print("query: ",p.query)
    print("Top-5 document URLs for the query: ",p.urls)
    #print(p.all_paras)
    print("Total number of paragraphs are: {}".format(p.num_paras))
    