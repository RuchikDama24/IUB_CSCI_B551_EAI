# ASSIGNMENT 2
Team:
Ruchik Dama (IU username : rdama)

Shashank Kumar (IU username : sk128)

Sumanth GopalKrishna (IU username : sgopalk)

# Part 1: Pikachu
In part 1, we are using the minimax algorithm to play the game .

The initial state: A NxN board where N>6

Successor states: Successor states are all the valid moves that can be played by the current player. If the player is white or black pichu it can move forward, left and right by one step. If there is an opponent pichu or pikachu in the neighbouring position and the next to next position is empty then it can capture the opponent piece and move 2 steps. A pichu becomes Pikachu if it reaches last row(for white), first row(for black). Pikachu can move forward,backward,left right with n steps and can capture opponent pichu pikachu and can move n steps.

State space: State space can be any combinations of white and black pikachus in the given board(If board is NxN then white and black pichus would be 2*N)

Goal State: Goal state for white would be no black pichus and pikachus and Goal state for black would be no white pichus and pikachus

Evaluation Functionn:((no. of white pichus)+4*(no. of white pikachus))-((no. of black pichus)+4*(no. of black pikachus))

### Successor Function
For the successor states we created a successor function:
Successors would be all valid moves played by the current player.

### is_goal function :
The Goal state is there are no white pichus and pikachus or there are no black pichus and pikachus

### Minimax function:
For Minimax Algorithm we Referred the following website:-
https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm
The values that are passed tho minimax are current_board,depth,targetdepth,maxplayer. Maxplayer is true if player is in "wW" else false
Minimax function is a recursive function that returns the (evaluation Function value when depth==targetdepth and also returns the board of that evaluation function)

### find_best_moves:
It yields the best move with the varying depth. The depth increases by 1 till it reaches the goal state.

# Part 2: The Game of Sebastian

### Problem-: 
It is a one player game of luck and skill which consists of four steps: rolling 5 dice, inspecting and choosing a subset of it and rolling it again and repeating this for another turn (total of 3 rolls). On the final dice combination, we assign one category out of the 13 and we repeat this for 13 turns until all the categories have been taken and we should make sure that none of the categories are repeated. 

### Strategy and Implementation:

The strategy used here is the Expectimax algorithm. We assume the player here is the max node. After the max nodes in the tree, there is a layer of chance nodes in the game tree. Here, we compute the expected values for all the chance nodes and take the maximum out of them and choose the path to the node having the maximum value.
To get all the chance nodes we take into consideration all the possible dice combinations using a nested for loop. We then call the function to compute the expected values for each node. Here, we take into consideration the probabilities of each child of the chance node and multiply it by the utility value of that node which we get from the Score() function. 

The Score() function computes the score of the dice combination to each category and assigns the category with the maximum value to the dice and returns the maximum value and the category. 
The sum of all the values is multiplied by the 1/(6** times the number of rerolls) to compute the expected value. 
The maximum of this is then taken and the indices of the rerolls which were rolled again for the max node is returned for the second roll and in the case of the third role, the category is assigned.
Once a category is assigned to a dice roll, it was dropped or not taken into consideration for computing the utility values as well as to assign to the third reroll.

Dictionary was used to store the scores of the dice rolls so that the scores could be used again for the same dice roll combinations in case they occurred , which would reduce the computation time.

### Problem faced :- 

Initially the program was taking longer than 20 minutes to run. Hence,a dictionary was used to store all the scores of the dice combinations which were already computed so that if next time we get a similar dice combination we can look it up in the dictionary and get the values faster. This method helped to reduce the time taken to run the program by half and it runs pretty quickly now.

### Other methods tried: 

1. An expectimax game tree with two levels consisting of 2 max nodes and 2 chance nodes was tried for the first reroll as the first reroll should take into account the possibilities of the second reroll as well. 
But this was computationally very heavy and it was taking too long to execute. It took almost half an hour for 1 game. Hence, did it not go ahead with this approach and rather used a game tree with a single level consisting of one max and one chance node.
2.  Also, tried to implement a technique to improve the scores by giving priority to the categories involving the bonus categories by checking if a certain number appears 3 times or more then we wanted to consider assigning the top 6 categories, but it did not improve the scores by much as it all depended on the random dice rolls and the current approach gave better results.
3.  Even tried to use the probability of a few categories into count while assigning the groups but all of which did not increase the scores by a noticeable margin.


# Part 3: Document Classification

The problem statement was to classify given message belongs to Westcoast or Eastcoast. Naïve Bayes classifier was used to classify the given labels.

## Implementation:

### Training Procedure:

1.	From the training data, we took all the unique occurrence of word in a list. Every unique space-delimited token was considered as word.
2.	For each word, we calculated the likelihood for each class i.e probability of a word given it belongs to a certain class. We stored these likelihoods in a dictionary.
3.	There may be cases where a word might occur only in one class. The probability of that word in the other class would be zero. To overcome this issue, we used Laplace smoothing.
4.	After calculating the likelihood, we calculated the priors of the classes. Now, we have trained our Naïve Bayes model

### Testing Procedure:

1.	We separated each message in test data as space-delimited token in a list of list format
2.	For each word in test data, we checked if it is present in training data, and then computed the posterior probability of that class. 
(Posterior of class A = Likelihood of all word| class A * Prior of the class A)
3.	If Posterior of class A > Posterior of class B, we assigned it to class A else class B
4.	We are able to achieve an accuracy of 82.43%


## Challenges:
1.	Initially, we divided the data into Westcoast and Eastcoast classes. And computed the likelihood based on the words present in Westcoast and Eastcoast list. 
Due to which we missed calculating the probablity of word which might occur only in one class and not in other class. My accuracy was at 69%.
2.	After combining all the unique words, we removed those words which were occurring less than 5 time. My accuracy came to 77%. But when I introduced Laplace smoothing, I was able to achieve an accuracy of 82.43%


