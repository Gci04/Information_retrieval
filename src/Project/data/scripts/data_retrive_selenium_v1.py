import time, os, pickle
import multiprocessing as mp
import numpy as np

from dataCrawler import * #contains IEEESeach, arXiv & ScienceDirect

def get_data_selenium(query):
    all_results = {}
    failed = 0
    while failed < 3 :
        try:
            ScienceDirect_docs = ScienceDirect("./")
            ScienceDirect_docs.search(query)
            all_results.update(ScienceDirect_docs.results)
            break
        except Exception as e:
            if getattr(ScienceDirect_docs,"browser_running",True) : ScienceDirect_docs.browser.close()
            ScienceDirect_docs.results = {}
            failed +=1

    failed = 0
    while failed < 3 :
        try:
            arXiv_docs = arXiv("./")
            arXiv_docs.search(query)
            all_results.update(arXiv_docs.results)
            break
        except Exception as e:
            if getattr(arXiv_docs,"browser_running",True) : arXiv_docs.browser.close()
            arXiv_docs.results = {}
            failed +=1

    failed = 0
    while failed < 3 :
        try:
            ieee_docs = IEEESeach("./")
            ieee_docs.search(query)
            all_results.update(ieee_docs.results)
            break
        except Exception as e:
            if getattr(ieee_docs,"browser_running",True) : ieee_docs.browser.close()
            ieee_docs.results = {}
            failed +=1

    return all_results

def main(save_dir="../"):
    pool = mp.Pool(mp.cpu_count())
    with open('./words.txt','r') as f:
        terms = f.read().splitlines()

    results = pool.starmap_async(get_data_selenium, [[term] for term in terms[:2]]).get()
    pool.close()

    #Join the data retrieved from different sources & Save to disk
    all_data = {}
    for r in results:
        all_data.update(r)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(os.path.join(save_dir,'raw_data_selenium_v1.pickle'),'wb') as handle:
        pickle.dump(np.array([i for i in all_data.items()]),handle,protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()
