Theory of Computing: Project 1 - SAT

Thomas Mercurio, Brooke Mackey, Jack Munhall


2SAT:
- The 2SAT.py program performed the 2SAT algorithm as described in the project document.
- The file input to the program was the file CNF/2SAT.cnf and the output of this program is CSV/2SAT.csv.
- The brute.py program was also run with the file CNF/2SAT.cnf to compare outputs.
  - Using the brute.py programs outputs to verify the 2SAT.py outputs, we found that our 2SAT.py algorithm correctly determined the satisfiability or unsatisfiability and the assigned values 100% of the time.
  - 50 of the WFFs were unsatisfiabile, while 50 of the WFFs were satisfiable.
- When the 2SAT.py program is run on the sudoku.cnf file, the ouput is....
  - 1,8,26,2,52,S,-1,92.75,1,0,0,1,0,1,1,0
  - This corrrectly corresponds to the valid sudoku solution.
  - The variables assignments are as follows...
    - x111 = 1
    - x112 = 2
    - x121 = 3
    - x122 = 4
    - x211 = 5
    - x212 = 6
    - x221 = 7
    - x222 = 8
