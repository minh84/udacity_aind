# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins is well described [here](http://www.sudokudragon.com/sudokustrategy.htm#XL2104). 
Here we re-exlain it by going through an example. Consider the following board

|     |  1  |  2  | 3   | 4    |  5  | 6   |   7  |   8 |  9  |
|:---:|:---:|:---:|:---:|:----:|:---:|:---:|:----:|:---:|:---:|
|  A  |  1  | 237 |  4  | 2357 | 9   | 257 |  27  | 6   |  8  |
|  B  |  9  |  5  |  6  |  27  | 1   |  8  |  27  | 3   |  4  |  
|  C  |  23 | 237 |  8  |  4   | 37  |  6  |  9   | 5   |  1  |
|  D  |  5  |  1  | 2379| 237  |347  | 279 |  34  | 8   |  6  |
|  E  |  8  |  37 | 379 |  6   |347  | 579 | 345  | 1   |  2  |
|  F  |  6  |  4  |  23 | 1235 | 8   | 125 |  35  | 9   |  7  |
|  G  |  7  |  8  |  1  |  9   | 2   |  3  |  6   | 4   |  5  |
|  H  |  4  |  9  |  5  |  17  | 6   |  17 |  8   | 2   |  3  |
|  I  |  23 |  6  |  23 |  8   | 5   |  4  |  1   | 7   |  9  |
    /
Let's look at the third column, we see that **F3** and **I3** are naked twins with possible value *23*.
This means if **F3** gets value 2(3) then **I3** must get value 3(2) so we get a local constraint

* **F3/I3** gets value 23
* combining with global constraint: third column must have each digit 1-9 only once 

This implies **D3** can only be *79* (instead of *2379*) and **E3** can only be *79* (instead of *379*). So we have reduced the search space for **D3** and **E3**. 

In above example, we only look at one unit, but we could go through each unit, check if any naked twins in a unit then for all other cells from the same unit we eliminate the naked twins value from it.

This is implemented inside `solution.naked_twins`. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Recall the constraint of Sudoku, we want to ensure for each unit contains all digit 1-9 (which implies each digit appears one time). 
For normal Sudoku, we have the following units

* 9 rows (each has 9 cells on same row)
* 9 columns (each has 9 cells on same column)
* 9 squares (each has 9 cells)

For diagonal sudoku, we want to ensure all digit 1-9 appears only once on the two diagonals. This can be done by adding
two units (each represents a diagonal)

* *A1, B2,..., I9*
* *A9, B8,..., I1*

By adding the above two units, each time we call `solution.eliminate` or `solution.only_choice` we ensure that the two diagonal also contains all different digits (which implies they contain 1-9 each digit once).
### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

