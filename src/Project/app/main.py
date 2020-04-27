import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle, os, string
from annoy import AnnoyIndex
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec


#load index and Annoy
index = AnnoyIndex(5, 'euclidean')
index.load('../model/index.ann')

#Load Documents
with open('../data/raw_data_filtered.pickle', 'rb') as handle:
    documents = pickle.load(handle)

#Load Doc to vec
model = Doc2Vec.load("../model/d2v.model")

app = Flask(__name__,static_url_path='',static_folder='../',template_folder='../templates')

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

def retrieve(query):
    clean_query = clean(query)
    relevant = index.get_nns_by_vector(model.infer_vector(clean_query),10)
    return documents[relevant]

@app.route('/submit', methods=['POST'])
def submit():
    query = request.form['projectFilepath']
    if query.strip() == '':
        return render_template('index.html',results = [] , SearchTxt = query)
    else:
        #get result
        results = retrieve(query)
        return render_template('index.html',results = results , SearchTxt = query )

@app.route('/',methods=['POST', 'GET'])
def home():
    print("i am in root")
    res_data = []
    return render_template('index.html',results = res_data ,SearchTxt ='')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
