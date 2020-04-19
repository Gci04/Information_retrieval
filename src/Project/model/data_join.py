import json, pickle, ast
import numpy as np

with open('arxivData.json') as f:
    arxivData = json.load(f)

arxivData = np.array([ [doc['id'], {'year':doc['year'], 'title':doc.get('title','None'), 'link': ast.literal_eval(doc['link'])[-1].get('href'), 'Abstract': doc['summary']}]for doc in arxivData])

#Scraped data
with open('raw_data.pickle','rb') as handler:
    old_data = pickle.load(handler)

new_data = np.vstack((old_data,arxivData))

with open('joined_raw_data.pickle', 'wb') as handle:
    pickle.dump(new_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
