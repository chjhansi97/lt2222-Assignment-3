import argparse
import pickle
import random

parser = argparse.ArgumentParser()
parser.add_argument("model_file", help = "")
parser.add_argument("test_file", help = "")
args = parser.parse_args()

consonants = ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 's', 't', 'v', 'x', 'y', 'z', 'h', 'r', 't', 'w', 'y']

def fetch_model(model_file):
    with open(model_file, "rb") as f:
        model = pickle.load(f)
    return model

def sample_lines(file_name, lines):
    with open(file_name, "rb") as f:
        read_lines = f.readlines()
        sample_list = []
        for line in read_lines:
            sample_list.append(line)
        sample_lines_list = random.sample(sample_list, lines)
    return sample_lines_list

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

def perplexity(model, test_samples):
    classes = model.classes_
    probs = []
    for i in range(0, len(test_samples)):
        pass

if __name__ =="__main__":
    test_data = fetch_model(args.model_file)
    sampled_lines = sample_lines(args.test_file, 10)
    selected_samples = create_samples(sampled_lines)