''' 
    This script creates samples, training set, testing set from a selected corpus. 
    We need five command line arguments to run the script. 
    Please try python sample.py --help to check the arguments.

    Ex. python sample.py UN-english.txt.gz 1000 20 test.pickle train.pickle
'''
import argparse
import random
import pickle
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help = "file to be processed and create samples.")
parser.add_argument("lines", type=int, help = "number of sample lines to be processed")
parser.add_argument("test_percent", type=int, help = "test percent to split the samples")
parser.add_argument("test_file", help = "output with test data")
parser.add_argument("train_file", help = "output with train data")

args = parser.parse_args()

consonants = ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 's', 't', 'v', 'x', 'y', 'z', 'h', 'r', 't', 'w', 'y']

def sample_lines(file_name, lines):
    file = gzip.open(file_name,"rb")
    lines_list = list(file)
    sample_list = []
    for line in lines_list[:lines]:
        sample_list.append(line)
    samples = random.sample(sample_list, lines)
    return samples

def create_samples(sample_lines_list):
    all_samples = []
    for sample in sample_lines_list:
        for i in range(0, len(sample)-4):
            char_1 = sample[i] + "_"+str(1)
            char_2 = sample[i+1] + "_"+str(2)
            char_3 = sample[i+2] + "_"+str(3)
            char_4 = sample[i+3] + "_"+str(4)
            for char in sample[i+4:]:
                if char in consonants:
                    next_consonant = char
                    break
                else:
                    continue
            consonant_sample = (char_1, char_2, char_3, char_4, next_consonant)
            all_samples.append(consonant_sample)
    return all_samples
    
def split_samples(samples, test_size):
    percent = round(len(samples) * (test_size/100))
    train = samples[percent:]
    test = samples[:percent]

    return (train, test)

def train_test_data(train, test, train_file, test_file):
    with open(train_file, 'wb')as f:
        pickle.dump(train, f)
    with open(test_file, 'wb') as f:
        pickle.dump(test, f)

if __name__ == "__main__":
    sampled_lines = sample_lines(args.file_name, args.lines)

    full_samples = create_samples(sampled_lines)

    train, test = split_samples(full_samples, args.test_percent)

    train_test_data(train, test, args.test_file, args.train_file)
