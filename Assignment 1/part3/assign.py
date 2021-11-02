#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by:  Code by: Ayush Sanghavi sanghavi, Vighnesh Kolhatkar vkolhatk, Ruchik Dama rdama
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
# Discussed the logic with Shashank Kumar.

import sys
import time
import itertools
import copy
import heapq as hq

def read_file(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = {"team_w":l[1].split("-"),"team_nw":l[2].split(",")}
        return people

def successor(people_list,people):
    successors=[]
    c=[i for i in itertools.combinations(people_list,2)]
    for x in c:
        merged_team = [x[0]+ x[1]]
        if len(merged_team[0])>3:
            #print(merged_team)
            continue
        pending_team=[]
        for each_team in people_list:
            common_element=[]
            #print(each_team)
            for each_member in each_team:
                #print(each_member)
                if each_member in merged_team[0]:
                    common_element.append(each_member)
                    #print(common_element)
            if common_element == []:
                #print(common_element)
                pending_team.append(each_team)
                #print(pending_team)
        new = pending_team + merged_team
        #print(pending_team,"-----",merged_team,"-----",new)
        successors.append(new)
    #successors.append(new)
    return(successors)

def calculate_cost(groups, people):
    #print(groups)
    #group_complaints = {}
    #print(groups)
    complaints = 0
    for group in groups:
            #print(group)
            for person in group:
                    #print(person,1)
                    size = len(people[person]['team_w'])
                    like_people= copy.deepcopy(people[person]['team_w'])
                    while "zzz" in like_people:
                        like_people.remove("zzz")
                    dislike_people = copy.deepcopy(people[person]['team_nw'])
                    if "_" in dislike_people:
                        dislike_people.remove("_")
                    if size != len(group):
                        complaints = complaints+1
                    for every_person in like_people:
                        if every_person not in group:
                            complaints = complaints + 1
                    for every_person in dislike_people:
                        if every_person in group:
                            complaints = complaints + 2
            #group_complaints[tuple(group)] = complaints
    return(complaints)


def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (number of complaints) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    people = read_file(input_file)
    start_state = list(people.keys())
    fringe = []
    for index, item in enumerate(start_state):
        start_state[index] = [item]
    hq.heapify(fringe)
    hq.heappush(fringe, (calculate_cost(start_state, people), start_state))
    explored = []
    cost_f = 999
    while len(fringe) > 0:
        (cost, curr_state) = hq.heappop(fringe)
        # print(curr_state)
        explored.append(curr_state)

        # print(curr_state)
        result_state = []
        '''if curr_state==start_state:
            for i in curr_state:
                result_state.append(i[0])
            yield({"assigned-groups": result_state,
                       "total-cost" : cost})'''
        for i in curr_state:
            result_state.append("-".join(i))

        # Simple example. First we yield a quick solution
        if cost_f > cost:
            cost_f = cost
            yield ({"assigned-groups": result_state,
                    "total-cost": cost})
        for succ in successor(curr_state, people):
            if succ in explored:
                continue
            else:
                if calculate_cost(succ, people) < cost:
                    hq.heappush(fringe, (calculate_cost(succ, people), succ))


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
