import os, time, re , pickle, string
from nltk.corpus import stopwords

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from abc import ABCMeta, abstractmethod

#For arxiv & ScienceDirect API
import arxiv
from abc import ABCMeta, abstractmethod
from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
from elsapy.elssearch import ElsSearch

"""Create an Abstract Data Crawler
This class serves as a template to implement a specific scientific articles base crwaler
"""

class DataCrawler(metaclass=ABCMeta):
    """Base searcher to be used for all academic databases crawlers."""
    def __init__(self, output_directory, base_url):
        self.output_directory = output_directory
        self.base_url = base_url
        self.results = {}
        self.browser_running = True

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

#IEEEXplore Crawler class
class IEEESeach(DataCrawler):
    """IEEE document base searcher"""
    def __init__(self,output_dir):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        self.url = "https://ieeexplore.ieee.org"
        self.browser = webdriver.Chrome(executable_path='./chromedriver',chrome_options=options)
        self.browser.maximize_window()
        super().__init__(os.path.join(output_dir, 'IEEE'),self.url)

    def search(self,query="A Lightweight Autoencoder",max_res=100):
        """finds documents related to query in IEEE document base"""

        self.browser.get("https://ieeexplore.ieee.org")
        self.browser.implicitly_wait(10) #wait 10 sec for website to load
        input_element = self.browser.find_element_by_class_name("Typeahead-input") #find the query input field
        input_element.send_keys(query) #pass the query to input field

        action = ActionChains(self.browser).send_keys(Keys.ENTER)
        action.perform() #press search button

        #get all the urls of the articles/documents found
        for item in self.browser.find_elements_by_class_name("List-results-items")[:max_res]:
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
        self.browser_running = False

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

# arXiv data crawler class
class arXiv(DataCrawler):
    """arXiv.org document base searcher"""
    def __init__(self,output_dir):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.url = "https://arxiv.org"
        self.browser = webdriver.Chrome(executable_path='./chromedriver',chrome_options=options)
        self.browser.maximize_window()
        super().__init__(os.path.join(output_dir, 'arXiv'),self.url)

    def search(self,query="A Lightweight Autoencoder",max_res = 100):
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
        for r in res_art[:max_res]:
            try:
                doc_id = str(hex(time.time().as_integer_ratio()[0]))
                title = r.find_element_by_class_name("title").text
                abstract = r.find_element_by_class_name("abstract").text[10:-6]
                pdf_link = r.find_element_by_partial_link_text("pdf").get_attribute("href")
                dates = r.find_element_by_css_selector("p.is-size-7").text
                self.results[doc_id] = {"title": title, "year": dates, "link": pdf_link, "Abstract":abstract}
            except Exception as e:
                continue

        self.browser.quit()
        self.browser_running = False

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

#ScienceDirect Data crawler
class ScienceDirect(DataCrawler):
    """sciencedirect.com document base searcher"""
    def __init__(self,output_dir):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.url = "https://www.sciencedirect.com"
        self.browser = webdriver.Chrome(executable_path='./chromedriver',chrome_options=options)
        self.browser.maximize_window()
        super().__init__(os.path.join(output_dir, 'sciencedirect'),self.url)

    def search(self,query="A Lightweight Autoencoder",max_res=100):
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
        res_items = self.browser.find_elements_by_class_name("ResultItem")[:max_res]
        time.sleep(0.01)
        for i in res_items:
            try:
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
            except Exception as e:
                continue

        self.browser.quit()
        self.browser_running = False

    def filter_by_year(self):
        """extract any text if any .pdf, """
        print("Coming soon!!")

    def save(self):
        """Saves processed data."""
        print("Saving....")

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
