import re

from erros import CircularReferenceError
from utills import Utills
from copy import deepcopy

NOT_EVALUATED = 0
EVALUATED = 1
EVALUATING = 2



class Spreadsheet:
    """
       ` A simple spreadsheet evaluator.

       Supported cell values:
       - A numeric string (e.g. "5") -> evaluates to int(5)
       - Empty string ("") -> evaluates to 0
       - A formula starting with "=" which can have:
           * A single reference: =A1
           * A reference plus a number: =A1+5, =A1-3
           * Two references: =A1+B2, =B2-A3
           * A number plus a reference: =10+B2, =10-A1

       Only '+' or '-' operators are supported. its very easy to add more

       Columns are labeled A, B, C, ..., Z, AA, AB, ...
       Rows start at 1 (not zero-based😞).

       Circular references (e.g., a cell indirectly referring to itself) are detected and raise CircularReferenceError.
       """

    def __init__(self, data: list[list[str]]):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

        #check that all rows have the same number of columns
        if any(len(row) != self.cols for row in data):
            raise ValueError("All rows must have the same number of columns")

        # values[r][c] will store the computed integer value of cell (r, c)
        self.values = [[0] * self.cols for _ in range(self.rows)]

        self.state = [[NOT_EVALUATED] * self.cols for _ in range(self.rows)]

    def parse_reference(self, ref: str) -> tuple[int, int]:
        """
        Parse a cell reference like "A1", "B2", "AA10" into (row_index, col_index), zero-based.

        Raises ValueError if invalid or out of range.
        :param ref: the cell reference
        :return: a tuple (row_index, col_index)
        """
        match = re.match(r"([A-Za-z]+)([0-9]+)", ref)
        if not match:
            raise ValueError(f"Invalid reference: {ref}")

        col_part, row_part = match.groups()
        col_index = Utills.convert_26_base_to_decimal(col_part) - 1  # zero-based
        row_index = int(row_part) - 1  # zero-based

        if not (0 <= row_index < self.rows and 0 <= col_index < self.cols):
            raise ValueError(f"Reference out of range: {ref}")

        return row_index, col_index

    def _evaluate_token(self, token: str) -> int:
        """
        Evaluate a single token (either a reference or a number).
        :param token: the token to evaluate
        :return: the integer value of the token
        """
        ref_pattern = r"^[A-Za-z]+[0-9]+$"
        if re.match(ref_pattern, token):
            rr, cc = self.parse_reference(token)
            return self.evaluate_cell(rr, cc)
        else:
            # Try a number
            try:
                return int(token)
            except ValueError:
                raise ValueError(f"Invalid token: {token}")

    def _evaluate_formula(self, formula: str) -> int:
        """
        Evaluate a formula without the leading '='.

        Supported patterns:
          - Single reference or number
          - Reference operator number
          - Reference operator reference
          - Number operator reference

        Only one operator is allowed per formula.
        """
        operators_available = r"(\+|-)" # to add more operators add them here
        tokens = re.split(operators_available, formula)
        tokens = [t.strip() for t in tokens if t.strip()]

        if len(tokens) == 1:
            # single token - reference or number
            return self._evaluate_token(tokens[0])
        elif len(tokens) == 3:
            # token1 operator token2
            left_val = self._evaluate_token(tokens[0])
            op = tokens[1]
            right_val = self._evaluate_token(tokens[2])

            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            else: # to add more operators add them here in elif
                raise ValueError(f"Invalid operator '{op}'. Only '+' and '-' are supported.")
        else:
            raise ValueError(f"Invalid formula: {formula}")

    def evaluate_cell(self, r: int, c: int) -> int:
        """
        Evaluate cell (r, c). Return its integer value.
        Detects circular references via state.
        """
        if self.state[r][c] == EVALUATED:
            return self.values[r][c]

        if self.state[r][c] == EVALUATING:
            # We've come back to a cell already in computation -> circular reference
            raise CircularReferenceError(f"Circular reference detected at cell {self._cell_name(r, c)}")

        self.state[r][c] = EVALUATING
        cell_content = self.data[r][c].strip()

        if cell_content == "":
            # Empty cell = 0
            value = 0
        elif cell_content.startswith("="):
            # It's a formula
            value = self._evaluate_formula(cell_content[1:])
        else:
            # It's a number
            try:
                value = int(cell_content)
            except ValueError:
                raise ValueError(f"Invalid cell value at {r + 1},{c + 1}: {cell_content}")

        self.values[r][c] = value
        self.state[r][c] = EVALUATED  # Corrected line
        return value

    def _cell_name(self, r: int, c: int) -> str:
        """
        Convert zero-based (r, c) to a spreadsheet cell label like A1, B2, ...
        """
        return f"{self._column_name(c)}{r+1}"

    def _column_name(self, c: int) -> str:
        """
        Convert zero-based column index to column label.
        """
        result = []
        n = c + 1
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result.append(chr(remainder + ord('A')))
        return "".join(reversed(result))

    def evaluate(self) -> list[list[int]]:
        """
        Evaluate the entire spreadsheet and return a 2D list of integers.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.state[r][c] != EVALUATED:
                    self.evaluate_cell(r, c)
        return self.values
