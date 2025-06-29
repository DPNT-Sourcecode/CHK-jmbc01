from solutions.HLO.hello_solution import HelloSolution
import pytest


class TestHello():
    def test_hello(self):
        assert 'Hello,' in HelloSolution().hello("Alice")

    def test_hello_with_name(self):
        assert HelloSolution().hello("Bob") == "Hello, Bob!"

    def test_hello_with_special_characters(self):
        with pytest.raises(UnicodeDecodeError):
            HelloSolution().hello(u"Example Characters : \xc3\xa9 \xc3\xa0 Ã© Ã")

    def test_empty_string(self):
        with pytest.raises(ValueError):
            HelloSolution().hello("")

    def test_string(self):
        with pytest.raises(TypeError):
            HelloSolution().hello(123)


