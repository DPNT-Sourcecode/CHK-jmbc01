
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_validate_parameter_skus(self):
        assert CheckoutSolution().checkout("") == 0
        assert CheckoutSolution().checkout(None) == -1
        assert CheckoutSolution().checkout(123) == -1
        assert CheckoutSolution().checkout("a") == -1
        assert CheckoutSolution().checkout("-") == -1

    def test_validate_each_sku(self):
        assert CheckoutSolution().checkout("Z") == -1
        assert CheckoutSolution().checkout("A1") == -1

    def test_calculate_total(self):
        assert CheckoutSolution().checkout("A") == 50
        assert CheckoutSolution().checkout("B") == 30
        assert CheckoutSolution().checkout("C") == 20
        assert CheckoutSolution().checkout("AB") == 80

    def test_convert_skus_to_list_of_dict(self):
        skus = "AABBC"
        expected = {
            'A': {'count': 2, 'price': 50},
            'B': {'count': 2, 'price': 30},
            'C': {'count': 1, 'price': 20}
        }
        # assert correct count for each sku
        result = CheckoutSolution().convert_skus_to_dict(skus)
        assert expected['A']['count'] == result['A']['count']
        assert expected['B']['count'] == result['B']['count']
        assert expected['C']['count'] == result['C']['count']

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

    def test_random_order(self):
        random_order = "ABCDCBAABCABBAAA"
        expected_A_7 = 200 + 100
        expected_B_5 = 45 + 45 + 30
        expected_C_3 = 60
        expected_D_1 = 15
        total_expected = (
            expected_A_7 + expected_B_5 + expected_C_3 + expected_D_1)
        assert CheckoutSolution().checkout(random_order) == total_expected

    def test_free_item(self):
        assert CheckoutSolution().checkout("EEB") == 80

    def test_multiple_free_items(self):
        assert CheckoutSolution().checkout("EEBEE") == 80 + 80

    def test_free_item_offer_no_qualifying_items(self):
        assert CheckoutSolution().checkout("E") == 40
        assert CheckoutSolution().checkout("B") == 30
        assert CheckoutSolution().checkout("EE") == 80
        assert CheckoutSolution().checkout("EB") == 70

    def test_multiple_discounts(self):
        assert CheckoutSolution().checkout("AAAAAAAA") == 330
        assert CheckoutSolution().checkout("AAAAAAAAA") == 380

    def test_multiple_free_deductions(self):
        assert CheckoutSolution().checkout("EEEEBB") == 160

