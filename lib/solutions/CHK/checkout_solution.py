
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
        if not isinstance(skus, list):
            raise TypeError("Input must be a list of SKUs")

        validated_skus = [sku for sku in skus if self.validate_skus(sku)]

        if not all(validated_skus):
            raise ValueError("Invalid SKUs provided.")

        # check for special offers
        # sum each product
        # sum the total
        return self.calculate_total(skus)

    def validate_skus(self, sku: str) -> bool:
        if not isinstance(sku, str):
            raise TypeError("Input must be a string")
        for sku in sku:
            if sku not in BASIC_PRICES:
                raise ValueError(f"Invalid SKU: {sku}")
        return True

    def calculate_total(self, skus: list) -> int:
        return sum(skus)



