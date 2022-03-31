'''
    This script fetches the test file, output of sample.py and also the trained model from train file.
    It calculates the recall, precision, f-measure of the trained model. 
    We need three command line arguments to run the script.

    Ex. python test.py 
'''

import argparse
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

parser = argparse.ArgumentParser()
parser.add_argument("test_file", help = "test output from sample.py") #test.pickle
parser.add_argument("trained_model", help = "trained_model file which is the output of train file.")
parser.add_argument("average_type", help = "choose between micro and macro")

args = parser.parse_args()

def fetch_test_data(test_file): #test_file is test from the output of sample.py
    with open(test_file, "rb") as f:
        test_data = pickle.load(f)
    return test_data

def fetch_trained_model(train_data): #train_data is train_output from train.py
    with open(train_data, "rb") as f:
        train_model = pickle.load(f)
    return train_model

def create_columns_rows(test_data):
    columns_list = []
    vector_list = []
    consonants_list = []
    for sample in test_data:
        columns_list.append(list(sample[:4]))
    columns = [item for sublist in columns_list for item in sublist]
    columns.append('pred_consonant')
    for sample in test_data:
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

def eval_model(model, X_test, y_test, average_type):
    model.fit(X_test, y_test)
    y_pred = model.predict(X_test)
    precision = metrics.precision_score(y_test, y_pred, average=average_type)
    recall = metrics.recall_score(y_test, y_pred, average=average_type)
    f_measure = metrics.f1_score(y_test, y_pred, average=average_type)
    precision_score = "Precision:"+ str(precision)
    recall_score = "Recall:"+str(recall) 
    f_measure_score = "F-measure:"+str(f_measure)
    print(precision_score,"\n", recall_score,"\n", f_measure_score)
    

if __name__ =="__main__":
    test_data = fetch_test_data(args.test_file)

    train_model = fetch_trained_model(args.model)

    X_test, y_test = create_columns_rows(test_data)

    evaluation = eval_model(train_model, X_test, y_test, args.average_type)
    