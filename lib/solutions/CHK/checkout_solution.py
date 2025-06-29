
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
            raise ValueError("Input cannot be empty")
        if not isinstance(skus, str):
            raise TypeError("Input must be a string containing SKUs")

        validated_skus = [sku for sku in skus if self.validate_each_sku(sku)]

        if not all(validated_skus):
            raise ValueError("Invalid SKUs provided.")

        # check for special offers
        # sum each product
        # sum the total
        unique_skus = set(skus)
        sub_totals = [
            {
                'sku': sku,
                'count': skus.count(sku),
                'price': BASIC_PRICES[sku],
                'has_offer': sku in SPECIAL_OFFERS,
            } for sku in unique_skus
        ]
        return self.calculate_total(sub_totals)

    def validate_each_sku(self, sku: str) -> bool:
        if not isinstance(sku, str):
            raise TypeError("Input must be a string")
        if sku not in BASIC_PRICES:
            raise ValueError(f"Invalid SKU: {sku}")
        return True

    def calculate_total(self, sub_totals: list) -> int:
        total = 0
        for item in sub_totals:
            if item['has_offer']:
                total -= self.apply_special_offer(item)
            total += item['price'] * item['count']

        return total

