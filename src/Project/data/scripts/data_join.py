import json, pickle, ast
import numpy as np

def main():
    try:
        with open('../arxivData.json') as f:
            arxivData = json.load(f)
    except Exception as e:
        print("failed to open arxivData.json wiht Exception: ", e)
        exit(1)

    arxivData = np.array([ [doc['id'], {'year':doc['year'], 'title':doc.get('title','None'), 'link': ast.literal_eval(doc['link'])[-1].get('href'), 'Abstract': doc['summary']}]for doc in arxivData])

    #Scraped data
    try:
        with open('../raw_data.pickle','rb') as handler:
            old_data = pickle.load(handler)

        new_data = np.vstack((old_data,arxivData))

        with open('../joined_raw_data.pickle', 'wb') as handle:
            pickle.dump(new_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print("failed for join and save data",e)

if __name__ == '__main__':
    main()
