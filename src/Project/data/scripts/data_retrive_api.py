import concurrent.futures
import time, pickle, os

import numpy as np
import multiprocessing as mp

from dataCrawler import *

TERMS = []
with open('./words.txt','r') as f:
    TERMS = f.read().splitlines()

def get_res(query):
    """Retieves articles containing a given query.
    :param query : string, query of interest
    :return : dict, with articles contents and descriptions
    """
    fail = 0
    while fail < 5 :
        try:
            arxiv = arXiv_API('./')
            scienceDirect = ScienceDirect_API('./')

            arxiv.search(query)
            setattr(arxiv, 'success', True)

            scienceDirect.search(query)
            setattr(scienceDirect, 'success', True)

            return {**scienceDirect.data, **arxiv.data}
        except Exception as exc:
            # if one source was succefull, return the content else retry
            if getattr(arxiv,'success',False):
                return arxiv.data
            elif getattr(scienceDirect,'success',False):
                return scienceDirect.data
            else:
                fail += 1
                time.sleep(3)
                continue
    return {}

def main():
    all_data = {}
    os.mkdir('../temp_dump')

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_result = {executor.submit(get_res, term): term for term in TERMS}
        for future in concurrent.futures.as_completed(future_to_result):
            url = future_to_result[future]
            try:
                data = future.result()
            except Exception as exc:
                print('{} generated an exception: {}'.format(url, exc))
            else:
                print('{} generated {} documents'.format(url, len(data)))
                # if data gets big, create a callback function and dump folder
                try:
                    with open(f'../temp_dump/{url.replace(" ","")}_{time.time()}.pickle','wb') as handle:
                        pickle.dump(data,handle,protocol=pickle.HIGHEST_PROTOCOL)
                except Exception as e:
                    with open(f'../temp_dump/{time.time()}.pickle','wb') as handle:
                        pickle.dump(data,handle,protocol=pickle.HIGHEST_PROTOCOL)

                all_data.update(data)

    # dump reuslt to disk
    with open(f'../raw_data{time.time()}.pickle','wb') as handle:
        pickle.dump(np.array([i for i in all_data.items()]),handle,protocol=pickle.HIGHEST_PROTOCOL)

# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('Time taken : {}'.format(end-start))
