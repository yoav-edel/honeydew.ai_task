class Utills:
    def __init__(self):
        pass

    @staticmethod
    def convert_26_base_to_decimal(s : str, number_="""
        Convert a string (e.g. "A", "B", ..., "Z", "AA", "AB", ...) to a number as if it's a 26 base number
        empty string is considered as 0
        :param s: the string to convert
        :return: the decimal number
        """) -> int:
        result = 0
        for c in s:
            if c.islower():
                c = c.upper()
            if not c.isalpha():
                raise ValueError(f"Invalid character: {c}. Only letters are allowed, e.g. A-Z")
            result = result * 26 + (ord(c) - ord('A') + 1)
        return result

    @staticmethod
    def convert_decimal_to_26_base(n : int) -> str:
        """
        Convert a number to a string (e.g. "A", "B", ..., "Z", "AA", "AB", ...) as if it's a 26 base number
        if zero, empty string is returned
        :param n: the number to convert
        :return: the string representation in 26 base
        """
        if n < 0:
            raise ValueError("Only non-negative numbers are allowed.")
        result = []
        while n > 0:
            n, r = divmod(n - 1, 26)
            result.append(chr(r + ord('A')))
        return "".join(reversed(result))