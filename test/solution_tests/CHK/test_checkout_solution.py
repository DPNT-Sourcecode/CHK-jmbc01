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

    def test_calculate_total(self):
        assert CheckoutSolution().checkout("A") == 50
        assert CheckoutSolution().checkout("B") == 30
        assert CheckoutSolution().checkout("C") == 20
        assert CheckoutSolution().checkout("AB") == 80

    def test_convert_skus_to_list_of_dict(self):
        skus = "AABBC"
        expected = [
            {'sku': 'A', 'count': 2, 'price': 50},
            {'sku': 'B', 'count': 2, 'price': 30},
            {'sku': 'C', 'count': 1, 'price': 20}
        ]
        # assert correct count for each sku
        result = CheckoutSolution().convert_skus_to_list_of_dict(skus)
        assert len(result) == len(expected)
        assert result[0]['sku'] == expected[0]['sku']
        assert result[0]['count'] == expected[0]['count']
        assert result[0]['price'] == expected[0]['price']
        assert result[1]['count'] == expected[1]['count']

    def test_has_special_offer(self):
        assert CheckoutSolution().has_special_offer(
            {'sku': 'A', 'count': 3, 'price': 50}) is True
        assert CheckoutSolution().has_special_offer(
            {'sku': 'B', 'count': 2, 'price': 30}) is True
        assert CheckoutSolution().has_special_offer(
            {'sku': 'C', 'count': 1, 'price': 20}) is False

    def test_calculate_total_with_special_offers(self):
        assert CheckoutSolution().checkout("AAA") == 130
        assert CheckoutSolution().checkout("AAABBB") == 175
        assert CheckoutSolution().checkout("AABBC") == 130
        assert CheckoutSolution().checkout("AABBBCC") == 175
        assert CheckoutSolution().checkout("AABBBCCDD") == 175 + 15
        assert CheckoutSolution().checkout("AABBBCCDDDD") == 175 + 15 + 15

