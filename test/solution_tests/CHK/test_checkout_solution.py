
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_validate_parameter_skus(self):
        assert CheckoutSolution().checkout("") == 0
        assert CheckoutSolution().checkout(None) == -1
        assert CheckoutSolution().checkout(123) == -1
        assert CheckoutSolution().checkout("a") == -1
        assert CheckoutSolution().checkout("-") == -1

    def test_validate_each_sku(self):
        assert CheckoutSolution().checkout("E") == -1
        assert CheckoutSolution().checkout("A1") == -1

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
        # order of items will be different
        # because we got the set of skus before we created a list
        assert len(result) == len(expected)
        for item in expected:
            assert item in result, f"Expected {item} not found in result"

    def test_has_special_offer(self):
        assert CheckoutSolution().has_special_offer(
            {'sku': 'A', 'count': 3, 'price': 50}) is True
        assert CheckoutSolution().has_special_offer(
            {'sku': 'B', 'count': 2, 'price': 30}) is True
        assert CheckoutSolution().has_special_offer(
            {'sku': 'C', 'count': 1, 'price': 20}) is False

    def test_calculate_total_with_special_offers(self):
        assert CheckoutSolution().checkout("AAA") == 130
        assert CheckoutSolution().checkout("AAABBB") == 130 + 45 + 30
        assert CheckoutSolution().checkout("AABBC") == 100 + 45 + 20
        assert CheckoutSolution().checkout("AABBBCC") == 100 + 45 + 30 + 40
        assert CheckoutSolution().checkout(
            "AABBBCCDD") == 100 + 45 + 30 + 40 + 30
        assert CheckoutSolution().checkout(
            "AABBBCCDDDD") == 100 + 45 + 30 + 40 + 60
        assert CheckoutSolution().checkout("") == 0


