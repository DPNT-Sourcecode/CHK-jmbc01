import pytest
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_validate_parameter_skus(self):
        with pytest.raises(ValueError) as e:
            CheckoutSolution().checkout("")
        assert str(e.value) == "Input cannot be empty"
        with pytest.raises(TypeError) as e:
            CheckoutSolution().checkout(123)
        assert str(e.value) == "Input must be a string containing SKUs"

    def test_validate_each_sku(self):
        with pytest.raises(ValueError) as e:
            CheckoutSolution().checkout("E")
        assert str(e.value) == "Invalid SKU: E"
        with pytest.raises(ValueError) as e:
            CheckoutSolution().checkout("A1")
        assert str(e.value) == "Invalid SKU: 1"




