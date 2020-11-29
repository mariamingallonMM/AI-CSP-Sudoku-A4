# AI-CSP-Sudoku-A4
Use a Constraint Satisfaction Problem (CSP) algorithm to resolve Sudokus

## Introduction
In this assignment we will focus on constraint satisfaction problems (CSP). We will implement the AC-3 and backtracking algorithms to solve Sudoku puzzles. The objective of the game is just to ﬁll a 9 x 9 grid with numerical digits so that each column, each row, and each of the nine 3 x 3 sub-grids (also called boxes) contains one of all of the digits 1 through 9. Visit [sudoku.com](https://www.sudoku.com) to get a sense of how the game works.

## Submission requirements
Write the main algorithm file called: driver.py, which intelligently solves Sudoku puzzles. 
The program will be executed as follows in Vocareum using Python 3.6:
$ python3 driver.py <input_string>

In the starter code folder, you will find the file sudokus_start.txt, containing hundreds of sample Sudoku puzzles to be solved. Each Sudoku puzzle is represented as a single line of text, which starts from the top-left corner of the board, and enumerates the digits in each tile, row by row. In this assignment, we will use the number zero to indicate tiles that have not yet been filled. For example, the Sudoku board in the diagram shown above is represented as the string:

00302060090030005001001806400... (and so on)

When executed as above, replacing "<input_string>" with any valid string representation of a Sudoku board (for instance, taking any Sudoku board from sudokus_start.txt), your program will generate a file called output.txt, containing a single line of text representing the finished Sudoku board and the algorithm name (AC3 or BTS, explained later) which solved the Sudoku board. You must use a single white space as a delimiter between the board and the algorithm name. For example, output.txt looks like:

167523849984176523325489671798315264642798135531642798476831952213957486859264317 BTS

(single line, separated by a single white space)

Since this board is solved, the string representation will contain no zeros. You may test your program extensively by using sudokus_finish.txt, which contains the solved versions of all of the same puzzles.

## Execute

There are two versions of the main 'driver.py' file:
- one which runs in Python 3.6 on Vocareum **![py36/driver.py](py36/driver.py)**.
- one which runs in Python 3.7 by just executing the file **![driver.py](driver.py)** on your IDE.

The **first one** is to be executed using $ python3 driver.py <input_string> in Vocareum, where <input_string> represents the puzzle board as a string of numbers.
**Note** that to run it in Vocareum, we first need to read the line from the 'sudokus_start.txt' and pass it to a local variable in bash ($line). The following is the code we use in Vocareum before executing driver.py:
$ line=$(awk 'NR==1 {print; exit}' sudokus_start.txt)

where NR == 1 is for the first line

then we call the variable by:
$ echo "$line"

and finally execute the .py file by:
$ python3 driver.py "$line"

The **second one** can be simply run from your IDE if you are using Python 3.7. It will take each line of ![sudokus_start.txt](data/sudokus_start.txt) and pass it on as a starting Sudoku puzzle board to be solved by the program. If you prefer to run line by line just uncomment the line 'board = boards[0]' from 'main' per the excerpt below

def main():

    #take a string as input data from sudokus_start.txt file
    #input_string = str(sys.argv[1]) 
    input_string = 'sudokus_start.txt'
    boards = get_boards(input_string)
    for board in boards:
    #board = boards[0]
        AI_solver(board)
    
if __name__ == '__main__':
    main()

## How

### AC-3 Algorithm (AC3)
First, implement the AC-3 algorithm. Test your code on the provided set of puzzles in sudokus_start.txt. To make things easier, you can write a separate wrapper script (bash, or python) to loop through all the puzzles to see if your program can solve them. As shown in sudokus_finish.txt, there are only 2/400 Sudoku boards which can be solved AC3 alone. Is this expected or unexpected?

### Backtracking Algorithm (BTS)
Now, implement backtracking using the minimum remaining value heuristic. The order of values to be attempted for each variable is up to you. When a variable is assigned, apply forward checking to reduce variables domains. Test your code on the provided set of puzzles in sudokus_start.txt. Can you solve all puzzles now?

## Important
### Precedence over BTS

To check how powerful BTS is compared to AC3, you must execute AC-3 algorithm before Backtracking Search algorithm. That is, your program looks like this:

assignment = AC3(given_sudoku_board)
if (solved(assignment))
          return "<filled sudoku board>" + " AC3"
assignment = BTS(given_sudoku_board)
          return "<filled sudoku board>" + " BTS" 

### A few notes on writing the algorithm

What it is really meant by "To check how powerful BTS is compared to AC3, you must execute AC-3 algorithm before Backtracking Search algorithm.", or at least my interpretation is as follows:

- Create a function/method (or a class) that executes AC3 as per Fig 6.3 in the AIMA book (including the function revise used inside the main AC3.
- Create a function that executes BTS as per Fig 6.5 in the AIMA book, so there is a backtracking-search and a backtrack function; the latter is called in the former.
- The backtrack function is actually where the 'search' for the solution happens.
- If you implement 'backtrack' per fig 6.5 in AIMA book, the first thing is actually to check that the puzzle at that stage is not already 'solved'.
- Then inside 'backtrack' call a function (e.g. 'get_unassigned') that gets you the values from the puzzle board which are 'unassigned'; it should give you the 'key' of the value (e.g. 'A1', 'A2', etc) and the domain of that value (e.g. [1,2,3,4]) which will depend on other values in the same row, column or 3x3 square. This is represented by "var < - SELECT-UNASSIGNED-VARIABLE(csp, assignment)" in the pseudo code of fig 6.5.
- Then for each 'var' in the 'domain of var', as given by the 'get_unassigned' function, assign the value to a copy of the starting 'csp' (e.g. local_assignment dict) and set the value of the 'unassigned' dict as False for the 'key' just assigned. 
- If the value 'var' is consistent with the assignment, then continue to call AC3 inside BTS (backtrack-search, backtrack). 
- Next, test if it has been able to 'solve' the puzzle. If AC3 alone is capable of resolving it, then return the result at that point. In that case, the 'method' will be 'AC3.
- If AC3 was not able to 'solve' the puzzle, then carry one with the puzzle in the state that AC3 has left it and call in 'backtrack' (recursively inside backtrack). Before doing that, check that the value is still consistent. 
- Note that you need to update the dict 'unassigned' with the latest puzzle achieved by AC3 before calling 'backtrack'. I was not doing that and I was passing on the starting 'unassigned' dict which did not align with the 'local_assignment' dict for the puzzle at that time. It cost me a few days to figure it out and I felt a bit hopeless for a while so if I can make someone avoid that error that would make very happy ;)
- Next, we test the resulting puzzle from calling 'backtrack'; if the result from 'backtrack' did not return a valid result (not empty), then we call 'forward_checking' as an additional inference to reduce the domain of the unassigned variables when we step out of the loop 'for each value in ORDER-DOMAIN-VALUES'. Again we apply 'forward_checking' on the latest version of the 'local_ssignment' and 'unassigned' dicts.  
- If the assignment is not consistent, ensure those values are reverted back to their original values and 'unassigned' status so that when we call 'get_unassigned' again we can try with a different domain. 
- Finally, when running 'get_unassigned' it is essential to order the (key, vars) results considering the length of the array/list 'vars' so that the 'keys' with the smallest domain (smallest length of the possible values) get assigned first. This will implement the 'minimum-remaining-values' (MRV) heuristic as explained in section 6.3.1. of the AIMA book. 

In Backtracking Search pseudocode, why unassign() is not at the same indentation level as assign()? Should it be at the same level?

The pseudocode in class slides is taken from AIMA (Artificial Intelligence: Modern Approach) textbook, and the textbook's unassign() function essentially means unassign_if_assigned(var, assignment). Since unassign_if_assigned() does no operation if var is not assigned, the pseudocode correctly works.
However, in some edition of the textbook, unassign() is placed at the same level as assign() as below:

![BTS pseudocode with indented unassign function](images/bts-unassign-with-indent.jpg)
BTS pseudocode with indented unassign function(source: official AIMA website)

You can choose an appropriate indentation level depending on your preference.

## References

- [Constraint-Satisfaction Problems in Python](https://manningbooks.medium.com/constraint-satisfaction-problems-in-python-a1b4ba8dd3bb) by [David Kopec](https://manningbooks.medium.com/?source=post_page-----a1b4ba8dd3bb--------------------------------).
- [AIMA online](http://aima.cs.berkeley.edu/python/csp.html).
