import numpy as np
import pandas as pd
import re
import string
import pickle
import os
from nltk.stem import PorterStemmer

class SentimentPipeline:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir,'static','model','model.pickle'),'rb') as f:
            self.model = pickle.load(f)
        with open(os.path.join(base_dir,"static","model","corpora","stopwords","english"),'r') as file:
            self.sw = file.read().splitlines()
        vocab = pd.read_csv(os.path.join(base_dir,"static","model","vacabulary.txt"),header=None)
        self.tokens = vocab[0].tolist()
        self.ps = PorterStemmer()

    def remove_punctuations(self,text):
        for punctuation in string.punctuation:
            text = text.replace(punctuation,"")
        return text

    def preprocessing(self,text):
        data = pd.DataFrame([text], columns=['tweet'])
        data['tweet'] = data['tweet'].apply(self.remove_punctuations)
        data['tweet'] = data['tweet'].apply(lambda x: " ".join(w.lower() for w in x.split()))
        data['tweet'] = data['tweet'].apply(lambda x: " ".join(re.sub(r'^https?:\/\/.*[\r\n]*', '', w, flags=re.MULTILINE) for w in x.split()))
        data['tweet'] = data['tweet'].str.replace("\\d+", "", regex=True)
        data['tweet'] = data['tweet'].apply(lambda x: " ".join(self.ps.stem(w) for w in x.split()))
        data['tweet'] = data['tweet'].apply(lambda x: " ".join(w for w in x.split() if w not in self.sw))
        return data['tweet']

    def vectorizer(self,ds):
        vectorized_list = []
        for sentence in ds:
            sentence_list = np.zeros(len(self.tokens))
            for i in range(len(self.tokens)):
                if self.tokens[i] in sentence.split():
                    sentence_list[i] = 1
            vectorized_list.append(sentence_list)
        return np.asarray(vectorized_list, dtype=np.float32)

    def prediction(self,txt):
        preprocess = self.preprocessing(txt)
        vectorized_text = self.vectorizer(preprocess)
        predicted = self.model.predict(vectorized_text)
        if predicted == 1:
            return "Negative"
        else:
            return "Positive"
