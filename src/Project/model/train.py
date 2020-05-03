import time, os, pickle, string
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from annoy import AnnoyIndex
import numpy as np
from nltk.corpus import stopwords


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

def main(data_folder='../data',save_dir='./'):
    """Doc to Vec
    Create a document to vector model for the retrieved data.
    Start by cleaning the data, then convert each document to TaggedDocument to be used in training the Doc2Vec model.
    Lastly save the model for further use in processing a query.
    """
    assert os.path.exists(data_folder), f'{data_folder} (folder) doesnt exist!'
    assert os.path.exists(os.path.join(data_folder,'raw_data_filtered.pickle')), f'Tain data not found in {data_folder}'

    # Read full data from disk
    try:
        with open(os.path.join(data_folder,'raw_data_filtered.pickle'),'rb') as handler:
            all_data = pickle.load(handler)
    except Exception as e:
        print('data read failed with Exception {}'.format(e))
        exit(1)

    all_data = [clean(doc.get('Abstract')) for _ , doc in all_data]

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(all_data)]

    # train a model
    model = Doc2Vec(documents,vector_size=5,window=5,min_count=1,workers=4)

    # clean training data and save model to disk
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    model.save(os.path.join(save_dir,'d2v.model'))

    # Create Index using Annoy
    # use Eiclidean distance for the index. Also multiple others allowed
    index = AnnoyIndex(5, 'euclidean')

    for i, row in enumerate(all_data):
        index.add_item(i,model.infer_vector(row))

    index.build(100) # number of trees

    # Save Index to disk
    index.save(os.path.join(save_dir,'index.ann'))

if __name__ == '__main__':
    main()
