
class SumSolution:

    def compute(self, x, y):
        if x is None or y is None:
            raise ValueError("Both x and y must be provided")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both x and y must be numbers")
        return x + y

