import pytest
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_checkout(self):
        with pytest.raises(ValueError):
            CheckoutSolution().checkout("")
        assert CheckoutSolution().checkout("A") == 50



