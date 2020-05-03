import requests
from bs4 import BeautifulSoup, SoupStrainer
import urllib.parse, re

def download(url):
    '''
    download html for given url
    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            return content
        else:
            return None
    except:
        return None

def main():
    '''
    Retrieve Calls For Papers in science and technology fields from http://wikicfp.com
    '''
    page_links= []
    for i in range(1,11):
        content = download(f'http://wikicfp.com/cfp/allcfp?page={i}')
        model_base = BeautifulSoup(content, parse_only=SoupStrainer('form'))
        page_links += [urllib.parse.urljoin('http://wikicfp.com', l.get('href')) for l in model_base.find_all('a')[:-4]]

    res = []
    for link in page_links:
        content2 = download(link)
        model2 = BeautifulSoup(content2, parse_only=SoupStrainer('table','gglu'))
        temp = []
        for tr in model2.find_all('tr')[:-2]:
            if 'categories' in tr.getText().lower() : continue
            temp_res = re.sub("\n+", "\n", tr.getText()).strip().split('\n')
            temp.append([temp_res[0].strip(),temp_res[-1].strip()])
        res.append(temp)

    # TODO: Save data for disk 

if __name__ == '__main__':
    main()
