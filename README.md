# Tarea_minimalizacion
# Formal Languages
## Assignment 1 – DFA Minimization (Kozen’s Algorithm, Lecture 14)

**Students:**  Isabella Cadavid Posada, Wendy Vanessa Atehortua Chaverra 

**Class Number:** C2566-SI2002-5730

---

## 1. Environment

- **Operating System:** Tested on Windows 11  
- **Programming Language:** Python 3.10+  
- **Tools/Libraries Used:**  
  - `collections` (Python standard library)

---

## 2. Running the Program

1. Clone or download this repository.  
2. Ensure that you have Python 3.10 or higher installed.  
3. Place the input file (`ejemplo.txt`) in the same directory as the program (`codigo.py`).  
   - The input file must follow the format specified in the assignment statement:
     - First line: number of cases.  
     - Then, for each case:
       1. Number of states.  
       2. Alphabet (symbols separated by spaces).  
       3. Final states (separated by spaces).  
       4. Transition table (n rows, one per state).  
4. Run the program
5. The program will read the DFA cases from ejemplo.txt and print the equivalent state pairs.

---

# Algorithm Explanation

This program implements the DFA minimization algorithm presented in Kozen (1997), Lecture 14.

- Input parsing:
Reads the number of states, alphabet, final states, and transition table.
Builds the transition function as a matrix indexed by state and symbol.

- Pair initialization:
Considers all unordered pairs of states (p, q).
Marks pairs as distinguishable if one is final and the other is not.

- Propagation (dependency graph):
For each pair (p, q), checks transitions under each symbol.
If (p, q) depends on (r, s) and (r, s) is marked, then (p, q) must also be marked.
This is efficiently propagated with a queue (deque).

- Equivalence extraction:
After propagation, the remaining unmarked pairs are equivalent states.
These are printed in lexicographic order.
Thus, the program outputs the set of equivalent states, which can be collapsed to obtain the minimized DFA.

References
Kozen, Dexter C. Automata and Computability.

   ```bash
   python codigo.py
