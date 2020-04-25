import time, os, selenium, requests, re , pickle, string
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from annoy import AnnoyIndex
import numpy as np
from nltk.corpus import stopwords

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from abc import ABCMeta, abstractmethod

"""Create an Abstract Data Crawler
This class serves as a template to implement a specific scientific articles base crwaler
"""

class DataCrawler(metaclass=ABCMeta):
    """Base searcher to be used for all academic databases crawlers."""
    def __init__(self, output_directory, base_url):
        self.output_directory = output_directory
        self.base_url = base_url
        self.results = {}

    @abstractmethod
    def search(self):
        """Search a given query using base_url"""
        pass

    @abstractmethod
    def filter_by_year(self):
        """Processes raw data. This step should create the raw dataframe with all the required features. Shouldn't implement statistical or text cleaning."""
        pass

    @abstractmethod
    def save(self):
        """Saves processed data."""
        pass

def clean(sentence):
    # convert to lower case
    tokens = [w.lower() for w in sentence.strip().split(' ')]

    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in stripped if not w in stop_words]

    return tokens

"""IEEEXplore Crawler class"""
class IEEESeach(DataCrawler):
    """IEEE document base searcher"""
    def __init__(self,output_dir):
        self.url = "https://ieeexplore.ieee.org"
        self.browser = webdriver.Chrome(executable_path='./chromedriver')
        super().__init__(os.path.join(output_dir, 'IEEE'),self.url)

    def search(self,query="A Lightweight Autoencoder"):
        """finds documents related to query in IEEE document base"""

        self.browser.get("https://ieeexplore.ieee.org")
        self.browser.implicitly_wait(10) #wait 10 sec for website to load
        input_element = self.browser.find_element_by_class_name("Typeahead-input") #find the query input field
        input_element.send_keys(query) #pass the query to input field

        action = ActionChains(self.browser).send_keys(Keys.ENTER)
        action.perform() #press search button

        #get all the urls of the articles/documents found
        for item in self.browser.find_elements_by_class_name("List-results-items"):
            text = item.text.split("\n")
            title = text[0].strip()
            year = text[3].split("|")[0].split(":")[1].strip()

            #Get document link
            doc_id = str(hex(time.time().as_integer_ratio()[0]))
            link = item.find_element_by_tag_name("a").get_attribute("href")
            self.results[doc_id] = {"year" : int(year), "link":link}
            self.results[doc_id]['title'] = title

        #retrieve abstract text for each article/document in the results
        for name, doc_info in self.results.items():
            self.browser.get(doc_info['link'])
            time.sleep(0.05)
            abstract_text = self.browser.find_element_by_class_name("abstract-text").text
            self.results[name].update({"Abstract":abstract_text.split("\n")[1]})

        self.browser.quit()

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

"""arXiv data crawler class"""
class arXiv(DataCrawler):
    """arXiv.org document base searcher"""
    def __init__(self,output_dir):
        self.url = "https://arxiv.org"
        self.browser = webdriver.Chrome(executable_path='./chromedriver')
        super().__init__(os.path.join(output_dir, 'arXiv'),self.url)

    def search(self,query="A Lightweight Autoencoder"):
        """finds documents related to query in arXiv document base"""

        self.browser.get(self.url)
        self.browser.implicitly_wait(10) #wait 10 sec for website to load
        input_element = self.browser.find_element_by_name("query") #find the query input field
        input_element.send_keys(query) #pass the query to input field

        action = ActionChains(self.browser).send_keys(Keys.ENTER)
        action.perform() #press search button

        #expand the result div to show full abstract text
        expand = self.browser.find_elements_by_partial_link_text('▽ More')
        for x in range(0,len(expand)):
            expand[x].click()

        #get all the urls of the articles/documents found
        res_art = self.browser.find_elements_by_class_name("arxiv-result")
        self.results = {}
        for r in res_art:
            doc_id = str(hex(time.time().as_integer_ratio()[0]))
            title = r.find_element_by_class_name("title").text
            abstract = r.find_element_by_class_name("abstract").text[10:-6]
            pdf_link = r.find_element_by_partial_link_text("pdf").get_attribute("href")
            dates = r.find_element_by_css_selector("p.is-size-7").text
            self.results[doc_id] = {"title": title, "year": dates, "link": pdf_link, "Abstract":abstract}

        self.browser.quit()

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

"""ScienceDirect Data crawler"""
class ScienceDirect(DataCrawler):
    """sciencedirect.com document base searcher"""
    def __init__(self,output_dir):
        self.url = "https://www.sciencedirect.com"
        self.browser = webdriver.Chrome(executable_path='./chromedriver')
        super().__init__(os.path.join(output_dir, 'sciencedirect'),self.url)

    def search(self,query="A Lightweight Autoencoder"):
        """finds documents related to query in science direct document base"""

        self.browser.get(self.url)
        self.browser.implicitly_wait(10) #wait 10 sec for website to load
        input_element = self.browser.find_element_by_name("qs") #find the query input field
        input_element.send_keys(query) #pass the query to input field

        action = ActionChains(self.browser).send_keys(Keys.ENTER)
        action.perform() #press search button

        #expand the result div to show full abstract text
        self.results = {}
        time.sleep(0.01)
        res_items = self.browser.find_elements_by_class_name("ResultItem")
        time.sleep(0.01)
        for i in res_items:
            wait = WebDriverWait(i, 10)
            i.find_element_by_css_selector("[aria-label=Abstract]").click()
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'preview-body-container')))

            abstract = element.find_element_by_tag_name("p").text
            title = i.find_element_by_class_name("result-list-title-link").text
            pdf_link = i.find_element_by_partial_link_text("Download PDF").get_attribute("href")

            date = " ".join([j.text for j in i.find_element_by_class_name("SubType").find_elements_by_tag_name('span')])
            date = re.findall('(?:January|February|March|April|May|June|July|August|September|October|November|December)[\s-]\d{2,4}', date)

            date = date[0] if len(date)> 0 else 'Unknown'
            doc_id = str(hex(time.time().as_integer_ratio()[0]))
            self.results[doc_id] = { "year": date, "Abstract":abstract, "link": pdf_link, "title": title }

        self.browser.quit()

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

def main():
    ScienceDirect_docs = ScienceDirect("./")
    ScienceDirect_docs.search()

    arXiv_docs = arXiv("./")
    arXiv_docs.search()

    ieee_docs = IEEESeach("./")
    ieee_docs.search()

    """Join the data retrieved from different sources  & Save to disk"""

    #Join all the crawled data
    all_data = {**ieee_docs.results, **arXiv_docs.results, **ScienceDirect_docs.results}
    with open('raw_data.pickle','wb') as handle:
        pickle.dump(np.array([i for i in all_data.items()]),handle,protocol=pickle.HIGHEST_PROTOCOL)

    """Doc to Vec
    Create a document to vector model for the retrieved data.
    Start by cleaning the data, then convert each document to TaggedDocument to be used in training the Doc2Vec model.
    Lastly save the model for further use in processing a query.
    """

    # Read full data from disk
    with open('joined_raw_data.pickle','rb') as handler:
        all_data = pickle.load(handler)


    all_data = [clean(doc.get('Abstract')) for _ , doc in all_data]

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(all_data)]

    # train a model
    model = Doc2Vec(documents,vector_size=5,window=2,min_count=1,workers=4)

    # clean training data and save model to disk
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    model.save("d2v.model")

    """Create Index using Annoy"""

    # use Eiclidean distance for the index. Also multiple others allowed
    index = AnnoyIndex(5, 'euclidean')

    for i, row in enumerate(all_data):
        index.add_item(i,model.infer_vector(row))

    index.build(20) # number of trees

    # Save Index to disk
    index.save('index.ann')

if __name__ == '__main__':
    main()
