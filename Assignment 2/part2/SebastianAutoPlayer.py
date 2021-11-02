# Automatic Sebastian game player
# B551 Fall 2020
# PUT YOUR NAME AND USER ID HERE!
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#
# this is one layer with comments
from SebastianState import Dice
from SebastianState import Scorecard
import random

class SebastianAutoPlayer:

      def __init__(self):
            pass  
        
      #Score Function: to calculate the scores for the dice roll with the parameters : dice_roll- dice combination, reroll_number: to check which function is calling the score function,
      #scorecard=holds all the score values, score_dict= dictionary which holds the computed scores for the different dice combinations so it can be reused again
      def score(self,dice_roll,reroll_number,scorecard,score_dict):
          s=Scorecard()
          score_card=scorecard.scorecard
          d=Dice()
          
          #if third rolls calls this score function, then the scoreboard is an object of type dice, else, if called from first or second reroll it is a list of dice rolls
          if (reroll_number=="third"): 
              d.dice=dice_roll.dice
          else:
              d.dice=dice_roll
          Categories = [ "primis", "secundus", "tertium", "quartus", "quintus", "sextus", "company", "prattle", "squadron", "triplex", "quadrupla", "quintuplicatam", "pandemonium" ]
          #checking if the score card list exists, as, in the first call the score card is not yet created
          if bool(score_card): 
              for i in score_card:
                  Categories.remove(i) #removing all those categories which have already been assigned in this game
          #calculate the scores for each category in this dice combination
          all_good=False       # var:all_good lets us know if the scores for this combination has already been computed and if it is present in the dictionary of pre computed scores
          if (reroll_number!="third") and d.dice in score_dict: 
              all_good=True
              for category in Categories: 
                  if category not in score_dict[d.dice]:
                     all_good=False
          if all_good is True: 
              s.scorecard=score_dict[d.dice]  #scores for the dice combination is already computed, hence retrieved from the dictionary
          else:
              for category in Categories: #call the record function of the class Scorecard to retrieve the scores of the dice combination
                  s.record(category,d)
              if (reroll_number!="third"):
                  score_dict[d.dice]=s.scorecard #store the scoreboard values of the dice in the dictionary 
          max_category=max(s.scorecard,key=s.scorecard.get) #choose the category with the max score from the scores computed from the categories which are yet to be assinged 
          if (reroll_number=="third"): #if called from 3rd reroll return the category with the max score else return the max score itself
              return max_category
          return(s.scorecard[max_category],score_dict)
      
      # Idea derived from expectation_of_reroll() function in program shown in the 
      # Discussion 8 Walkthrough of CSCI 551 - Spring 2021
      
      # Function to calculate the expectation value
      def expection_score_second_reroll(self,roll,reroll,scorecard,score_dict): 
          exp=0
          roll_dice=roll.dice
          reroll_score_dict=score_dict
          #compute the scores for the dice combinations with the given rerolls
          for outcome_a in ((roll_dice[0],) if not reroll[0] else range(1,7)):
              for outcome_b in ((roll_dice[1],) if not reroll[1] else range(1,7)):
                  for outcome_c in ((roll_dice[2],) if not reroll[2] else range(1,7)):
                      for outcome_d in ((roll_dice[3],) if not reroll[3] else range(1,7)):
                          for outcome_e in ((roll_dice[4],) if not reroll[4] else range(1,7)):
                              exp_score=(self.score((outcome_a,outcome_b,outcome_c,outcome_d,outcome_e),"second",scorecard,reroll_score_dict))
                              reroll_score_dict=exp_score[1]
                              exp+=exp_score[0]
          #calculate the expected value by multiplying the probabilty over all the rerolls and the sum of the scores of the dice rolls
          expected_value=exp*1/(6**sum(reroll))
          return(expected_value,reroll_score_dict)
      
      
      #Function to find the best possible rerolls for the first dice roll
      def first_roll(self, dice, scorecard):
            score_dict={}
            roll=dice
            current_max=(0,0) #holds the indices and the max value
            #compute all the possible rerolls or combinations possible for the dice roll
            possible_rerolls=[(roll_a,roll_b,roll_c,roll_d,roll_e) for roll_a in (True,False) for roll_b in (True,False) for roll_c in (True,False) for roll_d in (True,False) for roll_e in (True,False) ]
            for reroll in possible_rerolls:
                exp_score=(self.expection_score_second_reroll(roll,reroll,scorecard,score_dict))
                score_dict=exp_score[1]
                if(exp_score[0]>current_max[0]): #compute the maximum of the scores 
                    current_max=(exp_score[0],reroll) 
            #get the roll combination for which you got the maximum score (eg:-[1,2] means roll the 1st and 2nd die)
            reroll_index=[ i for i,j in enumerate(current_max[1]) if j is True] 
            return reroll_index # return the indices to re roll
        
      #Function to find the best possible rerolls for the second dice roll
      def second_roll(self, dice, scorecard):
            score_dict={}
            roll=dice
            current_max=(0,0) #tuple which holds the indices of the dice combination and the max value
            #compute all the possible rerolls or combinations possible for the dice roll
            possible_rerolls=[(roll_a,roll_b,roll_c,roll_d,roll_e) for roll_a in (True,False) for roll_b in (True,False) for roll_c in (True,False) for roll_d in (True,False) for roll_e in (True,False) ]
            for reroll in possible_rerolls:
                exp_score=(self.expection_score_second_reroll(roll,reroll,scorecard,score_dict))
                score_dict=exp_score[1]
                if(exp_score[0]>current_max[0]): #compute the maximum of the scores 
                    current_max=(exp_score[0],reroll) 
            #get the roll combination for which you got the maximum score(eg:-[1,2] means roll the 1st and 2nd die)
            reroll_index=[ i for i,j in enumerate(current_max[1]) if j is True] 
            return reroll_index# return the indices to re roll
        
      #return the best category for which the 3 rolled dice belongs to out of all the categories by choosing the maximum category value
      def third_roll(self, dice, scorecard): 
          score_dict={}
          scorecard_category=self.score(dice,"third",scorecard,score_dict)
          return scorecard_category

