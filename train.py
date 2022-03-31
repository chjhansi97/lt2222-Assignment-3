'''
    This script trains the samples retrieved from sample.py on a specified classifier.
    We need three command line arguments to run the script.

    Ex. python train.py train.pickle train_output svc
'''

import argparse
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

parser = argparse.ArgumentParser()
parser.add_argument("train_file", help = "train output file from sample.py ")#train.pickle
parser.add_argument("train_output", help ="a file to store the trained model, output of train.py") #train_output.pickle
parser.add_argument("kernel_type", help = "please choose nb or svc classifier.")

args = parser.parse_args()

def fetch_train_data(train_file):
    with open(train_file, "rb") as f:
        train_data = pickle.load(f)
    # with open(train_file) as f:
    #     contents = f.readlines()
    return train_data

def create_columns_rows(train_data):
    columns_list = []
    vector_list = []
    consonants_list = []
    for sample in train_data:
        columns_list.append(list(sample[:4]))
    columns = [item for sublist in columns_list for item in sublist]
    columns.append('pred_consonant')
    for sample in train_data:
        chars = sample[:4]
        consonant = sample[4]
        vector = []
        for column in columns:
            if column in chars:
                vector.append(1)
            elif column not in chars:
                vector.append(0)
            else:
                continue
        vector_list.append(vector)
        consonants_list.append(consonant)
    X = np.array(vector_list)
    y = np.array(consonants_list)
    return X,y

def train(X_train,y_train,kernel):
    if kernel == "SVC":
        clf = SVC(kernel='linear')
    elif kernel == "NB":
        clf = MultinomialNB()
    else:
        return
    model = clf.fit(X_train, y_train)
    return model

def model(model,trained_model ):
    with open(trained_model, 'wb')as f:
        pickle.dump(model, f)
    
if __name__ =="__main__":

    train_data = fetch_train_data(args.train_file)

    X, y = create_columns_rows(train_data)

    svc = train(X, y, kernel='SVC')

    nb = train(X, y, kernel = 'NB')

    save_model = model(args.kernel, args.train_output_nb)
