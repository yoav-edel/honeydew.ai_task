Simple Spreadsheet Evaluator
Overview
This project implements a Python program that simulates a simple spreadsheet.
It evaluates a matrix where each cell can contain:

A number (e.g., 5)
A reference to another cell (e.g., =A1)
A simple formula with + or - (e.g., =A1+B1, =A1+5)
An empty cell, which is treated as 0.
The program detects and rejects circular references - it happens when a cell references itself directly or indirectly.

Approach:
The program create the two matrices: one for the resualt and one containg the state of each cell - NOT_EVALUATED, EVALUATING, EVALUATED.
Then the program goes through each cell and evaluate it. If the cell is a number or an empty cell,
it is evaluated and marked as EVALUATED. If the cell is a reference to another cell, the program evaluates the referenced cell and then evaluates the cell itself.
If the cell is a formula, the program evaluates the elemnts in the formula and then evaluates the cell itself.
If during calculation we encounter a cell that is in state EVALUATING, we have a circular reference and the program raises an exception - CircularReferenceError.

Layout:
The project contains the following files:
spreadsheet.py - the main file containing the implementation of the spreadsheet.
spreadsheet_tester.py - a file containing tests for the spreadsheet.
errors.py - a file containing the definition of the CircularReferenceError exception.
utils.py - a file containing utility functions.

Run the tests:
To run the tests donwload the project and run the spreadtsheet_tester.py file.

Thank you 😊

