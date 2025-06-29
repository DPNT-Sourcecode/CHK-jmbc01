
BASIC_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
}

SPECIAL_OFFERS = {
    'A': [{
        'amount': 3,
        'price': 130,
    }, {
        'amount': 5,
        'price': 200,
    }],
    'B': [{
        'amount': 2,
        'price': 45,
    }],
}

FREE_ITEMS = {
    'E': [{
        'qualifying_amount': 2,
        'free_item': 'B',
        'free_item_amount': 1,
    }],
}


class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        if skus == "":
            return 0
        if not skus:
            return -1
        if not isinstance(skus, str):
            return -1
        validated_skus = [self.validate_each_sku(sku) for sku in skus]
        if not all(validated_skus):
            return -1
        sub_totals = self.convert_skus_to_list_of_dict(skus)
        return self.calculate_total(sub_totals)

    def validate_each_sku(self, sku: str) -> bool:
        if not isinstance(sku, str):
            return False
        if sku not in BASIC_PRICES:
            return False
        return True

    def convert_skus_to_list_of_dict(self, skus: str) -> list:
        return [
            {
                'sku': sku,
                'count': skus.count(sku),
                'price': BASIC_PRICES.get(sku)
            } for sku in set(skus)
        ]

    def has_special_offer(self, item: dict) -> bool:
        is_in_special_offers = item['sku'] in SPECIAL_OFFERS
        if not is_in_special_offers:
            return False
        amounts_qualifying = [
            offer['amount'] for offer in SPECIAL_OFFERS[item['sku']]]
        amount_qualifies = any(
            item['count'] >= amount for amount in amounts_qualifying)
        if not amount_qualifies:
            return False
        return True

    def calculate_with_special_offer(self, item: dict) -> int:
        special_offers = SPECIAL_OFFERS[item['sku']]
        if len(special_offers) == 1:
            special_offer = special_offers[0]
            total_with_offer, remaining_count = self.one_special_offer(
                item, special_offer)
            remaining_total = self.reminder_no_discount(item, remaining_count)
            total = total_with_offer + remaining_total
            return total

        # order special offers by amount descending
        special_offers_sorted = sorted(
            special_offers, key=lambda x: x['amount'], reverse=True)
        total = 0
        item_count = item['count']
        for offer in special_offers_sorted:

            if item_count == 0:
                break
            elif item_count < offer['amount']:
                continue
            else:
                total_with_offer, remaining_count = self.one_special_offer(
                    item, offer)
                item_count = remaining_count
                total += total_with_offer
        total += self.reminder_no_discount(item, item_count)
        return total

    def one_special_offer(self, item: dict, special_offer: dict) -> int:
        # how many sets of products could qualify for the special offer
        offer_count = item['count'] // special_offer['amount']
        total_with_offer = offer_count * special_offer['price']
        # remaining products
        remaining_count = item['count'] % special_offer['amount']
        return total_with_offer, remaining_count

    def reminder_no_discount(self, item: dict, count: int) -> int:
        # if no discount, return the total price
        return item['price'] * count

    def free_items_deduction(self, item: dict, sub_totals: list) -> int:
        if item['sku'] not in FREE_ITEMS:
            return 0
        free_items = FREE_ITEMS[item['sku']]
        deduction = 0
        for free_item in free_items:
            free_item_sku = free_item['free_item']
            qualifying_amount = free_item['qualifying_amount']
            if item['count'] < qualifying_amount:
                continue

            # how many items you get for free for set of qualifying items
            free_item_count = free_item['free_item_amount']

            # find the free item in sub_totals
            for sub_total in sub_totals:
                if sub_total['sku'] == free_item_sku:
                    available_free_items = sub_total['count']
                    if available_free_items < free_item_count:
                        continue
                    # if multiple sets - need to calculate the remainder
                    sets_of_free_items, _ = divmod(
                        available_free_items, free_item_count)
                    qualifying_count = sets_of_free_items * free_item_count
                    deduction += qualifying_count * sub_total['price']
                    break
        return deduction

    def calculate_total(self, sub_totals: list) -> int:
        total = 0
        for item in sub_totals:
            if self.has_special_offer(item):
                total += self.calculate_with_special_offer(item)
            else:
                total += self.reminder_no_discount(item, item['count'])
        for item in sub_totals:
            total -= self.free_items_deduction(item, sub_totals)

        return total




