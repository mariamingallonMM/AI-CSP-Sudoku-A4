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

## How

### AC-3 Algorithm (AC3)
First, implement the AC-3 algorithm. Test your code on the provided set of puzzles in sudokus_start.txt. To make things easier, you can write a separate wrapper script (bash, or python) to loop through all the puzzles to see if your program can solve them. As shown in sudokus_finish.txt, there are only 2/400 Sudoku boards which can be solved AC3 alone. Is this expected or unexpected?

### Backtracking Algorithm (BTS)
Now, implement backtracking using the minimum remaining value heuristic. The order of values to be attempted for each variable is up to you. When a variable is assigned, apply forward checking to reduce variables domains. Test your code on the provided set of puzzles in sudokus_start.txt. Can you solve all puzzles now?

## Important
### 1. Precedence over BTS

To check how powerful BTS is compared to AC3, you must execute AC-3 algorithm before Backtracking Search algorithm. That is, your program looks like this:

assignment = AC3(given_sudoku_board)
if (solved(assignment))
          return "<filled sudoku board>" + " AC3"
assignment = BTS(given_sudoku_board)
          return "<filled sudoku board>" + " BTS" 

### 2. Test-Run Your Code

To avoid wasting submission attempts, please test-run your code on Vocareum, and make sure it successfully produces an output file with the correct format. You can do this by hitting the RUN button, which simply executes your program with a sample input string containing a valid starting Sudoku board. After you hit RUN, when your program terminates, you should locate the output file within your working directory. Make sure the board and the algorithm name is separated by a single white space.

### 3. Grading Submissions

We will test your final program on 20 test cases. You can assume all test cases can be solved at least by BTS. Some of test cases might be solved by AC3 alone. Each input test case will be rated 5 points for a successfully solved board, and zero for any other resultant output. In sum, your submission will be assessed out of a total of 100 points. The test cases are no different in nature than the hundreds of test cases already provided in your starter code folder, for which the solutions are also available. If you can solve all of those, your program will most likely get full credit.

### 4. Time Limit

By now, we expect that you have a good sense of appropriate data structures and object representations. Naive brute-force approaches to solving Sudoku puzzles may take minutes, or even hours, to [possibly never] terminate. However, a correctly implemented backtracking approach as specified above should take well under a minute per puzzle. The grader will provide some breathing room, but programs with much longer running times will be killed.

## FAQ

Q. My code return different answers between my local computer and Vocareum! What's the cause?

A. Please check in whether there is a Python version difference between Vocareum and your computer. As of July 2017, we use Python 3.4 on Vocareum for our grading environment. If you use Python 3.6 or newer locally, you might need to keep in mind the Dictionary ordering difference introduced in Python 3.6. One student reported sorting the resulted dictionary resolved the difference.

Q. What does it mean to solve a sudoku instance by AC-3 alone?

A. We consider a sudoku instance is solved if each of unassigned variables has only one domain value after AC-3.

Q. My AC-3 has more than 1,000 constraints. It seems too much ... is this a correct approach?

A. Yes, it is a correct approach. Having thousands of constraints is usual in CSP solvers. If we express Sudoku's constraints in a concise way such as "each row/column/box must consist of all of the nine integers 1 through 9", it seems sudoku's constraints can be expressed in just this single constraint. However, AC-3 only recognizes constraints in the form of arcs (binary relations), so we have to decompose this constraint into numerous binary constraints.

Q. In Backtracking Search pseudocode, why unassign() is not at the same indentation level as assign()? Should it be at the same level?

A. The pseudocode in class slides is taken from AIMA (Artificial Intelligence: Modern Approach) textbook, and the textbook's unassign() function essentially means unassign_if_assigned(var, assignment). Since unassign_if_assigned() does no operation if var is not assigned, the pseudocode correctly works.

However, in some edition of the textbook, unassign() is placed at the same level as assign() as below:

![BTS pseudocode with indented unassign function](images/bts-unassign-with-indent.jpg)
BTS pseudocode with indented unassign function(source: official AIMA website)

You can choose an appropriate indentation level depending on your preference.

## References

- []() by []() for .
