"""
This code implements a Constraint Satisfaction Problem (CSP) algorithm to resolve Sudokus. 
Written using Python 3.7
needs to run as by executing:
$ python3 driver.py <input_string>
e.g. python3 driver.py "000000000302540000050301070000000004409006005023054790000000050700810000080060009"

<input_string> = a string from "sudokus_start.txt"

Algorithm returns a file called output.txt, containing a single line of text representing the finished Sudoku board and the algorithm name used (AC3 or BTS) which solved the Sudoku board. It prints a single white space as a delimiter between the board and the algorithm name.

Example of output.txt:
167523849984176523325489671798315264642798135531642798476831952213957486859264317 BTS
"""


# builtin modules
import os
import psutil
import requests
import sys
import math


# 3rd party modules
import pandas as pd
import numpy as np


def CSP():


    return




def main():

    #take a string as input data from sudokus_start.txt file
    input_string = str(sys.argv[1]) 
    
    #execute functions here

    


if __name__ == '__main__':
    main()