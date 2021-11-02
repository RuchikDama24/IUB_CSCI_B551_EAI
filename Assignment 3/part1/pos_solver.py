###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:
#Sumanth G -sgopalk,ruchik- rdama, shashank- sk128
# (Based on skeleton code by D. Crandall)
#


import random
import math
import copy
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Do the training!
    #
    def train(self, data):# Training with the train file to calculate the transition and emision probabilities  
        Combo=data # data =(("sumanth","verb"),("is","noun"))
        self.words_all=[] #contains a tuple of all the words
        self.pos_all=[]   #contains a tuple of all the pos
        for i in range(len(Combo)):
          self.words_all+=Combo[i][0]
          self.pos_all+=Combo[i][1]
    
        self.word_dict={}  #emission 
        self.transition_dict={} #transitions
        self.start_dict={}      #intial 
        self.pos_word_dict={} #pos and word combo
        
        #pos_all_count probability
        self.pos_all_count={}
        self.pos_all_count_probability={}
        for i in self.pos_all:
            if i not in self.pos_all_count:
                self.pos_all_count[i]=1
            else:
                self.pos_all_count[i]+=1
        
        
        
        #self.pos_all_count_probability # check if you have to do it
        #print(self.pos_all_count)
        
        for words,pos in Combo:  #loops through the tuples in this manner --((("a","b")-->words,("c","d")-->POS),((),()))
          for i in range(0,len(words)):
            if i==0: #to store the initial probabilites
              if pos[i] not in self.start_dict: 
                self.start_dict[pos[i]]=1
              else:
                self.start_dict[pos[i]]+=1
                
            if words[i] not in self.word_dict: #to initialise the words in the dictionary
              self.word_dict[words[i]]={}
              
            if pos[i] in self.word_dict[words[i]]:
              self.word_dict[words[i]][pos[i]]+=1
            else: 
              self.word_dict[words[i]][pos[i]]=1
            
            if i!=0:            #transition storing
              pos_combo=pos[i-1]+pos[i]
              if pos_combo not in self.transition_dict:
                self.transition_dict[pos_combo]=1
              else:
                self.transition_dict[pos_combo]+=1
              if words[i] not in self.pos_word_dict:
                self.pos_word_dict[words[i]]={}
              if pos_combo not in self.pos_word_dict[words[i]]:
                self.pos_word_dict[words[i]][pos_combo]=1
              else:
                self.pos_word_dict[words[i]][pos_combo]+=1
        
        #transition_dict
        self.transition_dict_probability={}
        for transition in self.transition_dict:
            self.transition_dict_probability[transition]=self.transition_dict[transition]/sum(self.transition_dict.values())
        #start_dict probability
        self.start_dict_probability={}
        for pos in self.start_dict:
            self.start_dict_probability[pos]=self.start_dict[pos]/sum(self.start_dict.values())
            
        #word_dict probability
        self.word_dict_probability={}
        for each_word in self.word_dict:
            self.word_dict_probability[each_word]={}
            for each_pos in self.word_dict[each_word]:
                self.word_dict_probability[each_word][each_pos]={}
                self.word_dict_probability[each_word][each_pos]=self.word_dict[each_word][each_pos]/self.pos_all_count[each_pos]
        #print(self.word_dict_probability)
        
        #pos_word_dict_probability self.pos_word_dict[word][pos_combo]/self.transition_dict[pos_combo]
        self.pos_word_dict_probability={}
        for each_word in self.pos_word_dict:
            self.pos_word_dict_probability[each_word]={}
            for each_combo in self.pos_word_dict[each_word]:
                self.pos_word_dict_probability[each_word][each_combo]={}
                self.pos_word_dict_probability[each_word][each_combo]=self.pos_word_dict[each_word][each_combo]/self.transition_dict[each_combo]
    
    # Calculate the log of the posterior probability of a given sentence
    def posterior(self, model, sentence, label): #calculates the score for each model
        if model == "Simple":  
            score=0
            for word,word_label in zip(sentence,label):
                if word in self.word_dict_probability and word_label in self.word_dict_probability[word]:
                    score+=-math.log(self.word_dict_probability[word][word_label])-math.log(self.pos_all.count(word_label)/len(self.pos_all))
            return score
        elif model == "HMM":  
            score=0
            for word,word_label in zip(sentence,label):
                if word in self.word_dict_probability and word_label in self.word_dict_probability[word]:
                    score+=-math.log(self.word_dict_probability[word][word_label])-math.log(self.pos_all.count(word_label)/len(self.pos_all))
            score-=15
            return score
        
        elif model == "Complex":
            score=0
            word,word_label=(sentence,label)
            for i in range(len(sentence)):
                if i==0:
                   score+=-math.log(self.word_dict_probability[word[i]][word_label[i]])-math.log(self.start_dict_probability[word_label[i]]) 
                else:
                    pos_combo=word_label[i-1]+word_label[i]
                    if pos_combo not in self.transition_dict_probability:
                        self.transition_dict_probability[pos_combo]=self.global_minima
                    if pos_combo not in self.pos_word_dict_probability[word[i]]:
                        self.pos_word_dict_probability[word[i]][pos_combo]=self.global_minima 
                    score+=-math.log(self.pos_word_dict_probability[word[i]][pos_combo])-math.log(self.transition_dict_probability[pos_combo])#else:            
            return score          
        else:
            print("Unknown algo!")
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence): #returns pos for each word in the sentence
        self.global_minima=0.0000001
        list_assigned=[] 
        pos_unique=set(self.pos_all)
        for word in sentence:
            minimum_score=math.inf
            for each_pos in pos_unique: #going through all the possibilities of the POS
              if word in self.word_dict_probability and each_pos in self.word_dict_probability[word]: #if only the word and the pos is there in the dictionary
                a=-math.log(self.word_dict_probability[word][each_pos])-math.log(self.pos_all_count[each_pos]/len(self.pos_all))
                if a<minimum_score: #storing the minimum value for the log probability
                  minimum_score=a
                  pos_assigned=each_pos
              if word not in self.word_dict_probability:#mostly the words not in the train set would be proper nouns so assiging that to them 
                  pos_assigned="noun"
                  self.word_dict_probability[word]={pos_assigned:self.global_minima} #adding the new word to the dictionary
              if word not in self.word_dict:#mostly the words not in the train set would be proper nouns so assiging that to them 
                  pos_assigned="noun"
                  self.word_dict[word]={"noun":1} #adding the new word to the dictionary
              if word not in self.pos_word_dict:#mostly the words not in the train set would be proper nouns so assiging that to them 
                  pos_assigned="noun"
                  self.pos_word_dict[word]={"noun":1}
            #pos_word_dict_probability
              if word not in self.pos_word_dict_probability:#mostly the words not in the train set would be proper nouns so assiging that to them 
                  pos_assigned="noun"
                  self.pos_word_dict_probability[word]={"pos_assigned":self.global_minima}
              
            list_assigned.append(pos_assigned)
        return(list_assigned)

    def hmm_viterbi(self, sentence):
        global_minima=0.0000001
        # matrix contaning index value of maximum state of previous column
        backtrack_matrix = np.ones((len(set(self.pos_all)), len(sentence)))
        # State probablity
        state_prob = np.ones((len(set(self.pos_all)), len(sentence)))
        pos_unique = list(set(self.pos_all))
        #print(pos_unique)
        # viterbi
        for col in range(0, len(sentence)):
            word = sentence[col]
            for row in range(0,len(pos_unique)):          
                maximum=-math.inf 
                each_pos = pos_unique[row]
                if col==0:
                    if each_pos not in self.word_dict_probability[word]:
                        self.word_dict_probability[word][each_pos]=global_minima
                    if each_pos not in self.start_dict_probability:
                        self.start_dict_probability[each_pos]=global_minima                   
                    a=(self.word_dict_probability[word][each_pos])*(self.start_dict_probability[each_pos])
                    state_prob[row][col]=a
                elif col!=0:
                    for j in range(len(pos_unique)):
                        each_pos_previous = pos_unique[j]
                        pos_combo=each_pos_previous+each_pos
                        if each_pos not in self.word_dict_probability[word]:
                            self.word_dict_probability[word][each_pos]=global_minima
                        if pos_combo not in self.transition_dict_probability:
                            self.transition_dict_probability[pos_combo]=global_minima                    
                        a=(state_prob[j][col-1])*(self.transition_dict_probability[pos_combo])
      
                        if a>maximum:
                            maximum = a
                            backtrack_matrix[row][col] = j
                    state_prob[row][col] = maximum*self.word_dict_probability[word][each_pos]#math.log(self.word_dict_probability[word][each_pos])

        max_state = np.argmax(state_prob[:, state_prob.shape[1] - 1])

        # backtracking the ridge

        pos_backtrack_index = np.ones(state_prob.shape[1])

        for col in range(state_prob.shape[1] - 1, -1, -1):
            pos_backtrack_index[col] = int(max_state)
            max_state = backtrack_matrix[int(max_state)][col]

        final_pos = []
        for i in pos_backtrack_index:
            final_pos.append(pos_unique[int(i)])

        return final_pos

    
    def gibbs(self,pos_sample,sentence):#alternate between the different possibilities of POS for each word 
        global_minima=0.000001
        pos_unique=set(self.pos_all)
        
        for i in range(1,100):
            pos_sample[i]=copy.deepcopy(pos_sample[i-1])
            
            for j in range(len(sentence)):
                min_prob=math.inf 
                word=sentence[j]
                for each_pos in pos_unique:                    
                     if j==0: #emission * initial
                        if each_pos not in self.word_dict_probability[word]:
                          self.word_dict_probability[word][each_pos]=global_minima
                        if each_pos not in self.start_dict_probability:
                          self.start_dict_probability[each_pos]=global_minima
                        a=-math.log(self.word_dict_probability[word][each_pos])-math.log(self.start_dict_probability[each_pos])
                     if j!=0 and j!=(len(sentence)-1):                         
                        pos_combo=pos_sample[i][j-1]+each_pos
                        pos_combo_next=each_pos+pos_sample[i][j+1]
                        if pos_combo not in self.pos_word_dict_probability[word]:
                          self.pos_word_dict_probability[word][pos_combo]=global_minima                        
                        if pos_combo not in self.transition_dict_probability:
                          self.transition_dict_probability[pos_combo]=global_minima
                          
                        #for next
                        next_word=sentence[j+1]
                        if pos_combo_next not in self.pos_word_dict_probability[next_word]:
                          self.pos_word_dict_probability[next_word][pos_combo_next]=global_minima                        
                        if pos_combo_next not in self.transition_dict_probability:
                          self.transition_dict_probability[pos_combo_next]=global_minima
                        a=-math.log(self.pos_word_dict_probability[word][pos_combo])-math.log(self.transition_dict_probability[pos_combo])-math.log(self.pos_word_dict_probability[next_word][pos_combo_next])-math.log(self.transition_dict_probability[pos_combo_next])
                        
                     if (j==(len(sentence)-1)):
                        pos_combo=pos_sample[i][j-1]+each_pos
                        if pos_combo not in self.pos_word_dict_probability[word]:
                          self.pos_word_dict_probability[word][pos_combo]=global_minima                        
                        if pos_combo not in self.transition_dict_probability:
                          self.transition_dict_probability[pos_combo]=global_minima
                        a=-math.log(self.pos_word_dict_probability[word][pos_combo])-math.log(self.transition_dict_probability[pos_combo])
                     if a<min_prob:
                        min_prob=a
                        pos_assigned=each_pos
                     
                pos_sample[i][j]=pos_assigned
        return(pos_sample)            
        
    def complex_mcmc(self, sentence):#this method called to do the gibbs sampling
        pos_sample=[[]]*100
        pos_sample[0]=["noun"]*len(sentence)
        pos_count={}
        Final_list_gibbs=[]
        pos_sample=self.gibbs(pos_sample,sentence)
        
        for words in sentence:
            pos_count[words]={}
            
        for i in range(50,len(pos_sample)):
            for j in range(0,len(sentence)):
                word=sentence[j]
                if pos_sample[i][j] not in pos_count[word]:
                    pos_count[word][pos_sample[i][j]]=1
                else:
                    pos_count[word][pos_sample[i][j]]+=1
        
        for i in sentence:
            Final_list_gibbs.append(max(pos_count[i],key=pos_count[i].get))
        return Final_list_gibbs
                


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence): #here you're finding the best possible sequence of POS and in the solver method you're finding the score of these
        if model == "Simple": #if simple model then calls the method in the solver simplified 
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

