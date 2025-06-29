
from solutions.CHK.checkout_solution import CheckoutSolution


class TestCheckout():
    def test_validate_parameter_skus(self):
        assert CheckoutSolution().checkout("") == 0
        assert CheckoutSolution().checkout(None) == -1
        assert CheckoutSolution().checkout(123) == -1
        assert CheckoutSolution().checkout("a") == -1
        assert CheckoutSolution().checkout("-") == -1

    def test_validate_each_sku(self):
        assert CheckoutSolution().checkout("A1") == -1

    def test_calculate_total(self):
        assert CheckoutSolution().checkout("A") == 50
        assert CheckoutSolution().checkout("B") == 30
        assert CheckoutSolution().checkout("C") == 20
        assert CheckoutSolution().checkout("AB") == 80

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

    def test_another_random_order(self):
        random_order = "ABCDECBAABCABBAAAEEAA"
        assert CheckoutSolution().checkout(random_order) == 665

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
        assert CheckoutSolution().checkout("AAAAAAAAAA") == 400

    def test_multiple_free_deductions(self):
        assert CheckoutSolution().checkout("EEEEBB") == 160
        assert CheckoutSolution().checkout("BEBEEE") == 160

    def test_free_item_same_as_trigger(self):
        assert CheckoutSolution().checkout("F") == 10
        assert CheckoutSolution().checkout("FF") == 20
        assert CheckoutSolution().checkout("FFF") == 20
        assert CheckoutSolution().checkout("FFFF") == 20 + 10
        assert CheckoutSolution().checkout("FFFFF") == 20 + 20
        assert CheckoutSolution().checkout("FFFFFF") == 20 + 20

    def test_multiple_offers(self):
        assert CheckoutSolution().checkout("STX") == 45
        assert CheckoutSolution().checkout("STY") == 45
        assert CheckoutSolution().checkout("STZ") == 45
        assert CheckoutSolution().checkout("STXY") == 45 + 17
        assert CheckoutSolution().checkout("STXZ") == 45 + 17
        assert CheckoutSolution().checkout("STYZ") == 45 + 20
        assert CheckoutSolution().checkout("STXYZ") == 45 + 17 + 20

    def test_mix_group_and_special_offers(self):
        assert CheckoutSolution().checkout("STXAAA") == 45 + 130

    def test_single_item(self):
        assert CheckoutSolution().checkout("S") == 20
        assert CheckoutSolution().checkout("T") == 20
        assert CheckoutSolution().checkout("X") == 17



