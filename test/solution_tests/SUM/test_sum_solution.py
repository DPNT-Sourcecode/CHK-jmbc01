from solutions.SUM.sum_solution import SumSolution
import pytest

class TestSum():
    def test_sum(self):
        assert SumSolution().compute(1, 2) == 3

    def test_string(self):
        with pytest.raises(TypeError):
            SumSolution().compute("a", "b")

