
BASIC_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
}

SPECIAL_OFFERS = {
    'A': {
        'amount': 3,
        'price': 130,
    },
    'B': {
        'amount': 2,
        'price': 45,
    },
}


class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        if not skus:
            return -1
        if not isinstance(skus, str):
            return -1

        validated_skus = [sku for sku in skus if self.validate_each_sku(sku)]

        if not all(validated_skus):
            raise ValueError("Invalid SKUs provided.")
        sub_totals = self.convert_skus_to_list_of_dict(skus)
        return self.calculate_total(sub_totals)

    def validate_each_sku(self, sku: str) -> bool:
        if not isinstance(sku, str):
            raise TypeError("Input must be a string")
        if sku not in BASIC_PRICES:
            raise ValueError(f"Invalid SKU: {sku}")
        return True

    def convert_skus_to_list_of_dict(self, skus: str) -> list:
        return [
            {
                'sku': sku,
                'count': skus.count(sku),
                'price': BASIC_PRICES[sku],
            } for sku in set(skus)
        ]

    def has_special_offer(self, item: dict) -> bool:
        is_in_special_offers = item['sku'] in SPECIAL_OFFERS
        if not is_in_special_offers:
            return False
        amount_qualifying = SPECIAL_OFFERS[item['sku']]['amount']
        amount_qualifies = item['count'] >= amount_qualifying
        if not amount_qualifies:
            return False
        return True

    def calculate_with_special_offer(self, item: dict) -> int:
        special_offer = SPECIAL_OFFERS[item['sku']]
        # how many sets of products could qualify for the special offer
        offer_count = item['count'] // special_offer['amount']
        print('offer_count:', offer_count)
        total_with_offer = offer_count * special_offer['price']
        print('total_with_offer:', total_with_offer)
        # remaining products
        remaining_count = item['count'] % special_offer['amount']
        print('remaining_count:', remaining_count)
        remaining_total = item['price'] * remaining_count
        print('remaining_total:', remaining_total)
        return total_with_offer + remaining_total

    def calculate_total(self, sub_totals: list) -> int:
        total = 0
        for item in sub_totals:
            if self.has_special_offer(item):
                total += self.calculate_with_special_offer(item)
            else:
                total += item['price'] * item['count']

        return total




