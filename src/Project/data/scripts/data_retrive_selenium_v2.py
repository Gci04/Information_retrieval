import datetime, itertools
from concurrent.futures import ProcessPoolExecutor, wait, ThreadPoolExecutor
import os, time, selenium, requests, re , pickle, string
import numpy as np

from dataCrawler import * #contains IEEESeach, arXiv & ScienceDirect

def run_process(query, target='arxiv'):
    if target == 'ieee':
        failed = 0
        while failed < 3:
            try:
                ieee_docs = IEEESeach("./")
                ieee_docs.search(query)
                return ieee_docs.results
            except Exception as e:
                print('IEEE error : ',e)
                if getattr(ieee_docs,"browser_running",True) : ieee_docs.browser.close()
                failed +=1
                continue
        return {}
    elif target == 'arxiv':
        failed = 0
        while failed < 3:
            try:
                arXiv_docs = arXiv("./")
                arXiv_docs.search(query)
                return arXiv_docs.results
            except Exception as e:
                print("arXiv error : ",e)
                if getattr(arXiv_docs,"browser_running",True) : arXiv_docs.browser.close()
                failed +=1
                continue
        return {}
    else:
        failed = 0
        while failed < 3:
            try:
                ScienceDirect_docs = ScienceDirect("./")
                ScienceDirect_docs.search(query)
                return ScienceDirect_docs.results
            except Exception as e:
                print("ScienceDirect error : ",e)
                if getattr(ScienceDirect_docs,"browser_running",True) : ScienceDirect_docs.browser.close()
                failed +=1
                continue
        return {}


if __name__ == '__main__':
    save_dir = '../'

    with open('./words.txt','r') as f:
        terms = f.read().splitlines()

    targets = ['ieee','ScienceDirect','arxiv']
    futures = []

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        for target, term in itertools.product(targets,terms[20:22]):
            futures.append(executor.submit(run_process, term, target))

    wait(futures)
    end_time = time.time()

    all_data = {}
    for r in futures:
        all_data.update(r.result())

    # Dump data to disk
    with open(os.path.join(save_dir,'raw_data_selenium_v2.pickle'),'wb') as handle:
        pickle.dump(np.array([i for i in all_data.items()]),handle,protocol=pickle.HIGHEST_PROTOCOL)

    print(f'Elapsed run time: {end_time - start_time} seconds')
