import time,pickle, os
import urllib.request as ur
import numpy as np
import multiprocessing as mp

from dataCrawler import *

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
