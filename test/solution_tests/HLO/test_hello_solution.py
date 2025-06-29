from solutions.HLO.hello_solution import HelloSolution
import pytest


class TestHello():
    def test_hello(self):
        assert HelloSolution().hello("Alice") == "Hello, world"

    def test_empty_string(self):
        with pytest.raises(ValueError):
            HelloSolution().hello("")

    def test_string(self):
        with pytest.raises(TypeError):
            HelloSolution().hello(123)

