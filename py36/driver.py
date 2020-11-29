"""
This code implements a Constraint Satisfaction Problem (CSP) algorithm to resolve Sudokus. 
Written using Python 3.7 and adapted to run in Vocareum needs to run as by executing:
$ python3 driver.py <input_string>
e.g. python3 driver.py "000000000302540000050301070000000004409006005023054790000000050700810000080060009"

<input_string> = a string from "sudokus_start.txt"

Algorithm returns a file called output.txt, containing a **single line*** of text representing the finished Sudoku board and the algorithm name used (AC3 or BTS) which solved the Sudoku board. It prints a single white space as a delimiter between the board and the algorithm name.

Example of output.txt:
167523849984176523325489671798315264642798135531642798476831952213957486859264317 BTS

Note that to run it in Vocareum, we first need to read the line from the 'sudokus_start.txt' and pass it to a local variable in bash ($line). The following is the code we use in Vocareum before executing driver.py:
line=$(awk 'NR==1 {print; exit}' sudokus_start.txt)

where NR == 1 is for the first line

then we call the variable by:
echo "$line"

e.g. python3 driver.py "$line"
"""

# builtin modules
import os
import psutil
import requests
import sys
import math
import copy
import types

# 3rd party modules
import pandas as pd
import csv
import numpy as np
from itertools import chain

class Queue:
   # class queue brought here to ensure code run in Vocareum on python 3.4. Queue implements a first-in-first-out (FIFO) queuing policy.
   # https://docs.python.org/2/tutorial/datastructures.html
   def __init__(self, initial):
      self.items = initial

   def contains(self, item):
      return item in self.items

   def empty(self):
      return len(self.items) == 0

   def push(self, item):
      self.items.insert(0,item)

   def pop(self):
      return self.items.pop()

   def size(self):
      return len(self.items)


# Set up x_keys and y_keys as global variables to use them accross all functions

global x_keys, y_keys

x_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
y_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
 

# Functions to setup the Sudoku board and the CSP main settings

def get_boards(filename:str = 'sudokus_start.txt'):

    input_path = os.path.join(os.getcwd(), 'data', filename)
    boards = pd.read_csv(input_path, sep=" ", header=None)

    boards = boards.values

    return boards

def setup_board(board:str):
    
    values = dict() # empty dict to assign the starting board
    index = 0
    for y in range(0, 9):
        for x in range(0, 9):
            n = board[0][index]
            if (n == "0"):
                val = np.arange(1,10)
            else:
                val = [int(n)]
            values[y_keys[y] + x_keys[x]] = val
            index += 1
    
    arcs = dict()
    for y in range(0, 9):
        for x in range(0, 9):
            key = y_keys[y] + x_keys[x]
            arcs[key] = get_neighbor_arcs(x, y)

    return values, arcs

def view_board(values:dict):
    title_row = " |  SUDOKU BOARD  | \n"
    top_row = " "
    for val in x_keys:
        top_row += " " + val
    top_row += "\n"
    
    result = title_row
    result += top_row
    result += " +-----+-----+-----+\n"

    for y in range(0, 9):
        result += y_keys[y] + "|"
        for x in range(0, 9):
            domain = values[y_keys[y] + x_keys[x]]
            if (len(domain) == 1):
                val = domain[0]
            else:
                val = 0

            result += str(val)
            if (x == 2 or x == 5 or x == 8):
                result += "|"
            else:
                result += " "
        if (y == 2 or y == 5 or y == 8):
            result += "\n +-----+-----+-----+\n"
        else:
            result += "\n"

    return print(result)


def get_neighbors(arcs:dict, Xi:int):
    result = []
    for (x,y) in arcs[Xi]:
        result.append(y)
    return result

def get_neighbor_arcs(Xi:int, Xj:int):
    arcs = dict()
    cell = y_keys[Xj] + x_keys[Xi]
    xoffs = (Xi // 3) * 3
    yoffs = (Xj // 3) * 3

    for x in range(0, 9):
        if (x != Xi):
            arcs[(cell, y_keys[Xj] + x_keys[x])] = 1
    for y in range(0, 9):
        if (y != Xj):
            arcs[(cell, y_keys[y] + x_keys[Xi])] = 1
    for x in range(xoffs, xoffs + 3):
        for y in range(yoffs, yoffs + 3):
            if (x != Xi or y != Xj):
                arcs[(cell, y_keys[y] + x_keys[x])] = 1
    return arcs.keys()

def get_arcs():
    result = []
    for y in range(0, 9):
        for x in range(0, 9):
            result += get_neighbor_arcs(x, y)
    return result

def revise(values:dict, Xi:int, Xj:int):
    D = list(values[Xi]) # define the domain D
    revised = False # set revised to False at the start

    for x in list(values[Xi]):
        for y in list(values[Xj]):
            if x != y:
                if x in D:
                    D.remove(x) # remove the value x from the domain
                revised = True # and set revised to True

    return revised, D

def solved(board_string:str):
    #when board is solved, no zeros will be in string 'board'
    #returns 'False' if '0' in board and 'True' otherwise to indicate puzzle is solved
    return (str('0') not in board_string) 


# Arc consistency algorithm AC-3

def AC3(values:dict, arcs:dict):
    """
    returns False if an inconsistency is found and True otherwise
    """
    q = Queue(get_arcs()) #queue all arcs in the csp
    while not q.empty():
        (Xi, Xj) = q.pop() #remove first value in queue
        bool, domain = revise(values, Xi, Xj)
        if bool:
            if (len(domain) == 0): # if domain has no values
                #print("AC3 inconsistency found!")
                return False
            for Xk in get_neighbors(arcs, Xi):
                q.push((Xk, Xi)) # add (Xk, Xi) to queue
        #print("AC3 no inconsistency found!")
    return True

# Backtracking Search algorithm

def BTS(values:dict, arcs:dict):
    """
    returns a solution or failure
    """
    unassigned = {}

    for key in values.keys():
        val = values[key]
        if 0 not in val:
            unassigned[key] = True
    
    method = 'BTS'

    #if len(unassigned) == 0:
    #    board_string = values_to_board(values)
    #    if solved(board_string):
    #        final_board = board_string 
    #        return (method, final_board)

    (method, final_board) = backtrack_search(unassigned, values, arcs)

    return (method, final_board)


def backtrack_search(unassigned:dict, values:dict, arcs:dict):

    # check if solved with local_assignment, and if so return results
    # first convert local_assignment values to a string
    if len(unassigned) == 0:
        board_string = values_to_board(values)
        if solved(board_string):
            final_board = board_string 
            method = 'BTS'
            return (method, final_board)
  
    # get the domain ('vars') of the first unassigned variable ('key')
    # get_unassigned uses minimum remaining values MRV and degree as heuristics
    (key, vars) = get_unassigned(values, unassigned)
    
    for var in vars:
        local_assignment = values.copy() 
        local_assignment[key] = [var] # add value of variable to assignment 'values'
        unassigned[key] = False # update unassigned for the key just assigned
        # if value is consistent with assignment then
        if (is_consistent(local_assignment, arcs, key, var)):
            # start solving using AC3 and note that 
            # if we have called backtrack_search it is because 
            # earlier attempts of solving the board with AC3 only did not succeed
            use_ac3 = AC3(local_assignment, arcs)
            unassigned = update_unassigned(local_assignment)
            #view_board(local_assignment)
            board_string = values_to_board(local_assignment)
            if solved(board_string):
                final_board = board_string
                method = 'AC3'
                return (method, final_board)
            # if we're still consistent, we recurse (continue)
            if (is_consistent(local_assignment, arcs, key, var)):
                board_string = values_to_board(values)
                if solved(board_string):
                    final_board = board_string
                    method = 'BTS'
                    return (method, final_board)
                # if we didn't find the result, we will end up backtracking
                else:
                    #first update the unassigned dict with the most recent local_assignment dict
                    unassigned = update_unassigned(local_assignment)
                    (method, final_board) = backtrack_search(unassigned, local_assignment, arcs)
                    if method is not None and final_board:
                        return (method, final_board)  
            # now we will apply 'forward_checking' (another more powerful type of inference)
            # to reduce the domain 'vars' of the variables in values/unassigned when stepping out of this loop. 
            saved_data = forward_checking(key, var, local_assignment, unassigned, arcs)
            for next_key in saved_data.keys():
                values[next_key] = saved_data[next_key]
        else:
            local_assignment[key] = values[key]
            unassigned[key] = True

    #final_board = values_to_board(values)

    return ('BTS', None)


# Helper functions for the backtracking search algorithm

def forward_checking(key:str, value:int, values:dict, unassigned: dict, arcs:dict):
    saved_data = dict()
    saved_data[key] = copy.copy(values[key])
    unassigned[key] = False

    values[key] = [value]
    for Xk in get_neighbors(arcs, key):
        index = 0
        domain = list(values[Xk])
        copied = False
        for domain_val in domain:
            if (domain_val == value):
                if not copied:
                    saved_data[Xk] = copy.copy(domain)
                    copied = True
                domain.pop(index)
            else:
                index += 1

    return saved_data


def get_unassigned(values:dict, unassigned:dict):
    """
    Select Unassigned Variable 
    It uses minimum remaining values MRV and degree as heuristics
    returns a tuple of:
    unassigned key and a list of the possible values
    e.g. ('a1', [1, 2, 3, 4, 5, 6, 7, 8, 9])
    """
    
    values_sort = dict() # empty dictionary to store length of possible values array

    for key in values.keys():
        length = len(values[key]) # get the length of possible values array 
        values_sort[key] = (length) # add to dictionary for sorting in next step

    # sort the dictionary including lengths of possible values from small to large
    # this is to later on assign the items with the minimum number of remaining values first
    values_sorted = dict(sorted(values_sort.items(), key=lambda item: item[1], reverse=False))

    for key in values_sorted.keys():
        if unassigned[key] == True:
            length = values_sorted[key]
            if length > 1:
                vars = values[key]
                return key, vars


# update unassigned

def update_unassigned(local_assignment:dict):

    unassigned = {}

    for k in local_assignment.keys():
                val = local_assignment[k]
                if len(val) == 1:
                    unassigned[k] = False
                if len(val) > 1:
                    unassigned[k] = True

    return unassigned

# check if value for given key is arc consistent

def is_consistent(values:dict, arcs:dict, key, value:int):
    result = True

    for Xk in get_neighbors(arcs, key):
        vals = values[Xk]
        if (len(vals) == 1 and vals[0] == value):
            result = False

    return result

def clone_values(values:dict):
    cloned_values = dict()
    for key in values.keys():
        newValues = []
        for nextValue in values[key]:
            newValues.append(nextValue)
        cloned_values[key] = newValues
    return cloned_values

def values_to_board(values:dict):
    result ="" # initiate the variable which will take the resulting string
    # iterate on dict values using the global variables y_keys and x_keys
    for y in range(0, 9):
        for x in range(0, 9):
            domain = values[y_keys[y] + x_keys[x]]
            if (len(domain) == 1):
                val = domain[0]
            else:
                val = 0
            result += str(val) # append to resulting string

    return result

# Write the outputs to a txt file per the assingment requirements

def write_txt(filename_outputs:str = 'output.txt', final_str:str = None):
    # write the outputs csv file
    filepath = os.path.join(os.getcwd(), filename_outputs)
    var = final_str
    with open(filepath, 'w') as out:
        out.write(var + '\n')
    return print("New Outputs file saved to: <<", filename_outputs, ">>", sep='', end='\n')

# The main function for the AI Sudoku solver. 
# We call all other functions from this one.

def AI_solver(board):
    """
    sudoku player using AC3 or BTS
    """
    values, arcs = setup_board(board)
    print("Start Board", end="\n")
    #view_board(values)
    print("First try with AC3 alone...", end="\n")
    use_ac3 = AC3(values, arcs) 
    board_string = values_to_board(values)
    if solved(board_string):
        method = 'AC3'
        final_str = ' '.join([str(board_string), method])
        write_txt('output.txt', final_str)
        print("This one was solved with AC3 alone!", end="\n")
        #view_board(values)
        return print(final_str)
    else:
        print("AC3 alone did not work so we try with backtrack and forward checking", end="\n")
        method, final_board = BTS(values, arcs)
        method = 'BTS'
        if solved(final_board):
            final_str = ' '.join([str(final_board), method])
            write_txt('output.txt', final_str)
            return print(final_str)


# Helper for executing this file from the terminal
def usage():
   print("python driver.py <input_string>")
   sys.exit(2)

###################################################

def main():

    #take a string as input data from sudokus_start.txt file
    input_string = str(sys.argv[1]) 
    board = np.array([input_string], dtype = object)
    if board:
        AI_solver(board)
    else:
        print("Enter valid command arguments !")
    
    
if __name__ == '__main__':
    main()
