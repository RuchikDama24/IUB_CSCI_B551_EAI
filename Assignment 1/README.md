# Assignment 1
Team: 

Ayush Sanghavi (IU username : sanghavi)

Vighnesh Kolhatkar (IU username : vkolhatk)

Ruchik Dama (IU username : rdama)

## Part 1:

In part 1, the search technique we used to solve the problem is the A* Search.
Let us formulate the search problem in terms of the following: 

1) The initial state: A jumbled 4x5 puzzle board.
2) Successor states: Successor states would be the set of all states that is obtained by
                       shifting the 1st and the 3rd row left shift or 2nd and 4th row right shift OR
                       the 1st, 3rd and 5th column shift up or the 2nd and the 4th column shift down.
3) State space: State space can be any combination of the numbers on the 4x5 board.
4) Cost function : The cost function here is uniform.
5) Goal State: Goal state = [1, 2, 3, 4, 5]
                            [6, 7, 8, 9,10]
                            [11,12,13,14,15]
                            [16,17,18,19,20]
6) Heuristic function : Number of misplaced tiles at any given point in time.

### For the successor states we created a successor function:
The successor states would be all the states possible that can be moved from the initial state to the goal state.
It could be moving the the rows or columns in the way they can move.

--> The following has been referred from the misere tic tac toe code. 
The list indexing in row and column shift functions are referred from tic tac toe code
---x--- Reference help ends here ---x---
For rowLeftShift, we use the indices and append the one element that needs to be shifted left, to the others that shift right by one index.
For rowRightShift, we used the indices and append the one element that needs to be shifted right, to the others that shift left by one index.


For column shifts, we first transpose the column and then call the right shift method for the 2nd and 4th row and then again transpose it to get the desired column.
For the 1st,3rd and 5th column, we first transpose the column and then call the left shift method for the 1st, 3rd and the 5th row and then again transpose it to get the desired column.
--> Transpose function used from the misere tic tac toe code.

### We created a function called oneDtotwoD that converts a single one dimensional list to a two dimensional list.

### Next, we created a heuristic function,
where if the current state is not equal to the goal state, then h(heuristic) is the sum of number of misplaced tiles.

### is_goal function :
The is_goal function takes the current state as the parameter and then checks if the current state, converts it to 2 dimensional and checks if it is the desired goal state or no.

### solve function : 
The solve function is where we create an empty list, that is the fringe.
We use the heapq module. The property of this is that each time, the smallest of heap element is popped(min heap). Whenever elements are pushed or popped, heap structure in maintained. The heappush takes in two parameters, our fringe, which is the location where the our data needs to be stored.
The fringe takes in the heuristic of initial state (the sum of the number of misplaced tiles), cost, initial state, and an empty list to store the path of the one that is popped first by the heapq.



## Part 2

For part 2, we first modify and perform some data pre-processing.

1) The initial state: We have the data of all roads in USA and the locations of all cities. We have the start city and end city with the cost function that has to be applied.
2) Successor states: Successor states are all the possible roads that leave from the current city
3) State space: The state space would be all routes given in the data.
4) Cost function : There are four cost functions:- distance, time, no. of segments, safest route to be taken
5) Goal State: Goal state = Goal state is to find the optimum solution from start city to end city, based on the cost function we provided.
6) Heuristic function : As there are four cost functions, we have four heursitic functions for all the cost functions.

We use pandas to read the data and put it into a dataframe called "city_gps".

We use pandas to read the data and put it into a dataframe called "roads".

### Challenges in data:
* We tried using a function to calculate the time and probability of successor cities, but somehow the values were not getting updated as expected.
  So, we added an extra column in the dataframe named 'time' and 'accidents'. 
  
* We tried putting everything in the same dataset.

* There were missing values in city-gps.txt and so we added all the values from road-segments.txt to city-gps.txt, dropped the duplicate values.
  We then set the missing values to 0. 
  
* However, while running the heuristic functions on that dataset we were not able to estimate the cost priority based on the output values. Since, the 
  fringe was not popping values as expected (i.e. min value of the cost_priority)

* Thus, we dropped the idea, of concatenating the datasets. Instead, we used 2 separate datasets, which were 'roads' and 'city_gps'. To tackle the issue of
  missing values, where certain cities does not have latitude and longitude values, we used a try-catch block in the respective heuristic functions itself.
  

We have used heapq to implement priority queue, where the root node returns the minimum value and based on that the values are popped. So, we set the first
parameter as cost_priority in all the heuristic functions.

Our current state will be the start state. We initialise the route_taken as an empty list, a fringe as an empty list, we heapify the fringe to set the priority, and create an empty list called explored.

We then push everything initialised into the fringe.


We have 4 functions for scenarios where segments, distance, time and safe are our cost functions.

In all the 4 functions, the while loop runs till the fringe is not empty. It explores the list of successors of the current city. 


For segment as our cost function, 

We created a function named segment_heuristic() , we calculate the average segment distance for the entire 'roads' data. Here, the haversine distance is calculated

and we divide the haversine distance between the cities by the average segment distance and add this to the cost of segment i.e. 1. This becomes our cost_priority.


For distance as our cost function, 
We created a new function called distance_heuristic() that calculates the distance between two places when their latitudes and longitudes are given (Haversine Formula) 

This distance is added to the distance reached till the current state which becomes the cost_priority. This iterates till the goal state is not reached.


For time as our cost function, 
We created a function named time_heuristic() , and calculated the haversine distance divided by max speed.

Here, the cost priority is the sum of time taken in hours to reach the current state and division of haversine distance by max speed.


For safe as our cost function, 

We created a function named safe_heuristic()

It iteratively updates the sum of probability of accidents till the current state and the sum of probability of accidents in interstate and non-interstate 
For interstate the probability is 0.00001 and for non inter state the probability is 0.00002.


All the 4 functions keep a track of the route taken, total miles travelled, time taken to reach and total expected accidents in hours which is calculated iteratively based on the cities explored,   
 

If city == goal (destination), we return all of the values calculated above.
else, we push everything in the fringe.





## Part 3

1) Initial State: A text file with people and their preferrences.
2) Successor function : Successor functions returns more optimized matches of the teammates from the current state.
3) State Space: Possible matches with team mates.
4) Cost function : Number of complaints.

Firstly, we read a file and pass the filename as the parameter. We created dictionary of name people. The people's dictionary will store the key as the student's name and the value will be everything (Preferred partner, unpreferred partner, information about open to work with anyone or open to work alone) than the student's name. 
We split the data by spaces, "-" and "," accordinly.
The function returns the people (dictionary).

### successor function:

The successor function takes in two parameters. We created an empty list called successor.
We define c, c is a list, which will contain combination of all pairs of all elements of people_list in groups of two.

Itertools is a module in python. It is used to iterate over data structures that can be stepped over using a for-loop. Such data structures are also known as iterables. This module incorporates functions that utilize computational resources efficiently. 
Definition: https://www.educative.io/edpresso/what-are-itertools-in-python

Now, x will iterate through c,
merged_team is a list of x[0] + x[1].
if the length of merged_team > 3 at any given point in time , then we continue, i.e iterate again.
The pending_team is an empty list which will store all teams that will be eventually appended with the merged_team.
Now we will iterate over people_list (one of the parameter the successor function takes), we create an empty list called common_element.
We iterate over each_team, if an element is in the merged_team, then it will append to the common_element list.
If the common list is empty, we will append that to the pending_team.
New is a list of pending and merged team (appended with each other).
We append new to the successors and return successors.

### calculate_cost function:

Our aim is to reduce the number of complaints. It takes two parameters.
We initialise the complaints to 0 first. 
We then define size that calculates the length of desired team that the person in people want. We then create a while loop, for removing zzz from like_people - (incase the student has no specific person to work with, but wants some person, be it unknown).
We then define dislike_people where we will put in the name of the people who the person does not want to work with. 
We then calculate the number of complaints and return the same according to the rules given.

### solver function:
We used heapq module to structure our data into a heap and hence pop in the desired priority.
This function takes the name of a .txt input file in the format indicated in the assignment.
We have called our successor function and the calculate_cost function.


