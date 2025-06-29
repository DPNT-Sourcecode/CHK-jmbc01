from solutions.HLO.hello_solution import HelloSolution


class TestCheckout():
    def test_checkout(self):
        assert HelloSolution().checkout("A") == 50
