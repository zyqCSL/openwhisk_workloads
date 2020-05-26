from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import pandas as pd
import numpy as np 

from time import time
import re

cleanup_re = re.compile('[^a-z]+')
def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

def main(params):
    text = params['text']
    df = pd.read_csv('/tmp/reviews20mb.csv')
    print("read csv done")
    start = time()
    df_input = pd.DataFrame()
    df_input['x']  = [text]
    df_input['x'] = df_input['x'].apply(cleanup)

    df['train'] = df['Text'].apply(cleanup)
    tfidf_vect = TfidfVectorizer(min_df=50, max_features=2338).fit(df['train'])
    X = tfidf_vect.transform(df_input['x'])
    print("transform done")

    model = joblib.load('/tmp/lr_model.pk')
    print("model loaded")
    y = model.predict(X)
    latency = time() - start

    ret_val = {}
    ret_val['y'] = y
    ret_val['latency'] = latency
    return ret_val

if __name__ == '__main__':
    params = {}
    params['text'] = 'Just fine'
    print(main(params))