#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math 
import copy

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def read_data(fname): #to read data for train file
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w for w in line.split()])
        exemplars += [ (data[0::2], data[1::2]), ]

    return exemplars

def train(data): #training with all the probabilities
        Combo=data
        for words,pos in Combo:  #loops through the tuples in this manner --((("a","b")-->words,("c","d")-->POS),((),()))
          for i in range(0,len(words)):
            if i==0: #to store the initial probabilites
              if words[i][0] not in start_dict:
                 start_dict[words[i][0]]=1
              else:
                 start_dict[words[i][0]]+=1              
          
          sentence=" ".join(words) #joining all the words into one sentence
          for i in range(len(sentence)):
            if i!=0:
                letter_combo=sentence[i-1]+sentence[i]
                if letter_combo not in transition_dict: #transition probabilities
                    transition_dict[letter_combo]=1
                else:
                    transition_dict[letter_combo]+=1
                              
def similarity_measure(a,b): #to check the similarity between the test and train images and assign them probabilities accordingly
  img_prob=1
  correct_prob_star=1   #probability of 1 for exact match with star
  correct_prob_space=0.3 #probability of 0.3 for exact match with space
  wrong_prob=0.2        #probability of 0.2 for no match
  for i in range(len(a)):
    for j in range(len(a[i])):
        if a[i][j]!=b[i][j]: #if both the pixels match or not
          img_prob=img_prob*wrong_prob
        else:
          if (a[i][j]=='*'):
              img_prob=img_prob*correct_prob_star
          else:
              img_prob=img_prob*correct_prob_space
  return img_prob


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname) #send the train image file here (with all the 26 characters and special etc) 
test_letters = load_letters(test_img_fname)

#from here your code try to put it in functions and remove the global variables
TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "


start_dict={} #can i create a global variable
transition_dict={}
word_dict={}
letter_sequence=[]

print("Learning model...")
train_data=read_data(train_txt_fname)
train(train_data)

#print(train_letters)
## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!



#simple

for test_images in test_letters:
  minimum_score=math.inf
  for letters in TRAIN_LETTERS: #given the letters
    sim_prob=similarity_measure(test_images,train_letters[letters])
    a=-math.log(sim_prob)
    if a<minimum_score: #storing the minimum value for the log probability
      minimum_score=a
      letter_assigned=letters
  letter_sequence.append(letter_assigned) #appending all the letters to the list 
  

#HMM
  
global_minima=0.000001
list_scores_previous_all=[]
list_scores_best_overall=[]

print("Testing classifier...")

for i in range(len(test_letters)): #test_images in test_letters:
  list_scores_previous_all_temporary=[]
  minimum=math.inf
  for letters in TRAIN_LETTERS: #given the letters
    if i==0:
        sim_prob=similarity_measure(test_letters[i],train_letters[letters])
        #print(start_dict)
        if letters not in start_dict:
            start_dict[letters]=global_minima
        a=-math.log(sim_prob)-math.log(start_dict[letters]/sum(start_dict.values()))
        list_scores_previous_all_temporary.append((letters,a))
    elif i!=0:
        j=0
        for previous_letters in TRAIN_LETTERS: #running through each training letter
            sim_prob=similarity_measure(test_letters[i],train_letters[letters])
            letter_combo=previous_letters+letters
            if letter_combo not in transition_dict: #create a dictionary if it is not there already
                transition_dict[letter_combo]=global_minima
            a=-math.log(sim_prob)-math.log(list_scores_previous_all[j][1])-math.log(transition_dict[letter_combo]/sum(transition_dict.values()))
            j+=1
            if a<minimum:
                minimum=a
                list_scores_best_for_each_POS=(letters,a)#for each level best
        list_scores_previous_all_temporary.append(list_scores_best_for_each_POS)
  list_scores_previous_all=copy.deepcopy(list_scores_previous_all_temporary)
  list_scores_best_overall.append(min(list_scores_previous_all,key=lambda list_scores_previous_all:list_scores_previous_all[1]))#for overall best
Final_list=[x[0] for x in list_scores_best_overall]

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:

print("\n".join([ r for r in train_letters['o'] ])) 
            #train_letters is a 72 length list containing all the characters of the english alphabet
# Same with test letters. Here's what the third letter of the test data
#  looks like:
print("\n".join([ r for r in test_letters[4] ]))


simple_result="".join(letter_sequence)
hmm_result="".join(Final_list)

print("Simple: "+simple_result)
print("   HMM: "+hmm_result)


