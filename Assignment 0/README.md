# ASSIGNMENT 0
## ROUTE PICHU
Set of Valid States:- Set of states where the agent is on the "." or has reached the goal state.

Successor Function:- The function that accepts the Map and the current position of the agent and returns the possible positions where the agent can move by a single move while considering the obstacles like walls.

Cost Function:- The cost function between two positions is 1.

Goal State:- The goal state is where the agent reaches the location where video is being recorded or where agent reaches my location.

Initial State:- Initial state is where agent is in a starting position in a map of NxM grid with walls in between.

I referred Artificial Intelligence:  A modern Approach by Russell and Norwig.

I used the BFS algorithm to find the shortest path in the map.

ISSUE FACED:-
My Path String was always greater than my shortest distance.
an extra "U" was being added when the agent was on the last row.

First, I was adding the my path string in a variable then returning it.
The Issue was fixed when I called my path string method in the return statements of the search method.
I still do not know why an extra "U" was being added.

I added a moveString method that creates my path string.

The assumption we made is that there is always one agent and a goal location.

## ARRANGE PICHUS

Set of Valid States:- Set of states where no two agent can see each other, that means, they cannot see each other horizontally or vertically.

Successor Function:- The successor function takes the current map as the input and adds an extra agent on the map and returns the new map.

Cost Function:- The cost function between two postions is 1.

Goal state:- Goal state is the state where K agents are arranges such that no two agents can see each other.

Initial State:- The initial state is that 1 agent is on the map of NxM grid with walls and no. of agents are specified.

The Assumptions are:-
If the wall is between two agents then they cannot see each other.

I have created methods to check whether the certain point is valid or not.
It checks the column and row of that point, if an agent is found then it returns false and if a wall is found or it reaches the last row/column it returns true. 
I have used backward iteration to check the up and right side of the point.

I have created 3 methods,
valid_row:- It takes the map and the current cordinates as the input and It checks whether there are agents on that row
valid_column:-It takes the map and the current cordinates as the input and It checks whether there are agents on that column.
valid:- It takes the map and the current cordinates as the input and returns the and of valid_row and valid_column.

I had also created a list that stores all the locations of walls and I was using that list to check whether the loop reached a wall or not.
Then I just used "is" comparision to check whether the loop reached wall or not.


If the position is valid then an agent is placed there.
