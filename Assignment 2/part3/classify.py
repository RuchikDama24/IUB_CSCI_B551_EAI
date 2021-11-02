# classify.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, March 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


def likelihood(total_words, Westcoast_object, Eastcoast_object):
    word_count_westcoast = {}
    word_count_eastcoast = {}

    for words in total_words:
        count_westcoast = 0
        for sentence in Westcoast_object:
            if words in sentence:
                count_westcoast += 1
        word_count_westcoast[words] = count_westcoast

        count_eastcoast = 0
        for sentence1 in Eastcoast_object:
            if words in sentence1:
                count_eastcoast += 1
        word_count_eastcoast[words] = count_eastcoast

    prob_word_westcoast = {k: (value + 1) / (len(Westcoast_object) + 2) for k, value in word_count_westcoast.items()}
    prob_word_eastcoast = {k: (value + 1) / (len(Eastcoast_object) + 2) for k, value in word_count_eastcoast.items()}

    return prob_word_westcoast, prob_word_eastcoast


def classifier(train_data, test_data):
    Westcoast_object = [train_data['objects'][idx] for idx, element in enumerate(train_data['labels']) if
                        element == 'WestCoast']
    Eastcoast_object = [train_data['objects'][idx] for idx, element in enumerate(train_data['labels']) if
                        element == 'EastCoast']

    total_words = set([words for elements in train_data['objects'] for words in elements.split()])

    prob_word_westcoast, prob_word_eastcoast = likelihood(total_words, Westcoast_object, Eastcoast_object)

    prob_westcoast = len(Westcoast_object) / len(train_data['objects'])
    prob_eastcoast = len(Eastcoast_object) / len(train_data['objects'])

    test_words = [words.split() for words in test_data['objects']]

    return test_labels(test_words, prob_word_westcoast, prob_word_eastcoast, prob_westcoast, prob_eastcoast)


def test_labels(test_words, prob_word_westcoast, prob_word_eastcoast, prob_westcoast, prob_eastcoast):
    label = []
    for sentence in test_words:
        prob_w = 1
        prob_e = 1

        for word in sentence:
            if word in prob_word_westcoast.keys():
                prob = prob_word_westcoast.get(word)
                prob_w = prob * prob_w

            if word in prob_word_eastcoast.keys():
                prob = prob_word_eastcoast.get(word)
                prob_e = prob * prob_e

        prob_w = prob_w * prob_westcoast
        prob_e = prob_e * prob_eastcoast

        if prob_w > prob_e:
            label.append('WestCoast')
        else:
            label.append('EastCoast')

    return label


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))


