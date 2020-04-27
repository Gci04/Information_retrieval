import time, arxiv,pickle, os,tqdm
import urllib.request as ur
from abc import ABCMeta, abstractmethod
from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
from elsapy.elssearch import ElsSearch
import numpy as np
import multiprocessing as mp


class API(metaclass=ABCMeta):
    """docstring for Base API."""

    def __init__(self, output_directory, api_url):
        self.output_directory = output_directory
        self.api_url = api_url
        self.api_name = ""
        self.data = {}

    @abstractmethod
    def search(self):
        """Search a given query using base_url"""
        pass

    @abstractmethod
    def save(self):
        """Saves processed data."""
        pass

class arXiv_API(API):
    """docstring for arXiv_API."""
    def __init__(self, dir):
        self.api_key = 'None'
        super().__init__(dir,"http://export.arxiv.org/api")
        self.api_name = 'arxiv'
    def search(self,query="A Lightweight Autoencoder"):

        # url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query.split(" "))}'
        # response = ur.urlopen(url).read()
        results = arxiv.query(query=query, max_results=50)
        for doc in results:
            title = doc["title"]
            abstract = doc["summary"]
            pdf_link = doc['pdf_url']
            dates = doc["published"].split("-")[0]
            doc_id = str(hex(time.time().as_integer_ratio()[0]))
            self.data[doc_id] = {"title": title, "year": dates, "link": pdf_link, "Abstract":abstract}

    def save(self):
        pass

class ScienceDirect_API(API):
    """docstring for arXiv_API."""
    def __init__(self, dir):
        self.api_key = '902bdc6a538d5912287ddc22ba0f3698'
        super().__init__(dir,'https://dev.elsevier.com')
        self.api_name = 'Science Direct API'
        self.client = ElsClient(self.api_key)

    def search(self,query="A Lightweight Autoencoder"):
        doc_srch = ElsSearch(query,'sciencedirect')
        doc_srch.execute(self.client, get_all = False)
        for _,doc in doc_srch.results_df.iterrows():
            pii_doc = FullDoc(sd_pii = doc['pii'])
            if pii_doc.read(self.client):
                try:
                    abstract = " ".join(pii_doc.data['coredata']['dc:description'].split()[1:])
                    doc_id = str(hex(time.time().as_integer_ratio()[0]))
                    title = doc['dc:title']
                    pdf_link = doc['link']['scidir']
                    dates = doc['load-date'].split('-')[0]
                    self.data[doc_id] = {"title": title, "year": dates, "link": pdf_link, "Abstract":abstract}
                except:
                    pass
            else:
                print("Doc Skipped!!")

    def save(self):
        pass

all_data = {}
def collect_result(result):
    global all_data
    all_data.update(result)

def main(query):
    try:
        arxiv = arXiv_API('./')
        arxiv.search(query)
        #all_data.update(arxiv.data)

        scienceDirect = ScienceDirect_API('./')
        scienceDirect.search(query)
        #all_data.update(scienceDirect.data)
        # print(query)
        return {**scienceDirect.data, **arxiv.data}
    except:
        ## TODO: Set timeout to avoid infinite wait and loop
        time.sleep(5)
        return main(query)

if __name__ == '__main__':

    pool = mp.Pool(mp.cpu_count())
    with open('./words.txt','r') as f:
        terms = f.read().splitlines()

    results = pool.starmap_async(main, [[row] for row in terms]).get()
    pool.close()

    for r in results:
        all_data.update(r)

    with open(f'raw_data{time.time()}.pickle','wb') as handle:
        pickle.dump(np.array([i for i in all_data.items()]),handle,protocol=pickle.HIGHEST_PROTOCOL)
