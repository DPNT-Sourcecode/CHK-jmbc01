
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

FREE_ITEMS_PROMOTIONS = {
    'E': [{
        'qualifying_amount': 2,
        'free_item': 'B',
        'free_item_amount': 1,
    }],
}


class CheckoutSolution:
    basket: dict = {}
    unique_skus: set = set()

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
        self.unique_skus = set(skus)
        self.basket = self.set_basket(skus)
        return self.calculate_total()

    def validate_each_sku(self, sku: str) -> bool:
        if not isinstance(sku, str):
            return False
        if sku not in BASIC_PRICES:
            return False
        return True

    def set_basket(self, skus: str) -> dict:
        items_dict = {}
        for sku in self.unique_skus:
            items_dict[sku] = {
                'sku': sku,
                'count': skus.count(sku),
                'price': BASIC_PRICES.get(sku)
            }
        updated_basket = self._update_basket_with_free_items(items_dict)
        return updated_basket

    def _update_basket_with_free_items(self, basket) -> dict:
        updated_basket = basket.copy()
        for sku, item in basket.items():
            if sku not in FREE_ITEMS_PROMOTIONS:
                continue
            free_item_promotions = FREE_ITEMS_PROMOTIONS[sku]
            for promotion in free_item_promotions:
                print('running promotion:', promotion)
                free_item_amount = promotion.get('free_item_amount', 0)
                sku_free_item = promotion['free_item']
                items_in_basket = updated_basket.get(
                    sku_free_item, {}).get('count', 0)
                not_enough_in_basket_to_apply_promotion = (
                    items_in_basket < free_item_amount)
                if not_enough_in_basket_to_apply_promotion:
                    print('promotion cannot be used:', promotion)
                    continue
                qualifying_amount = promotion['qualifying_amount']
                actual_amount = item['count']
                if actual_amount < qualifying_amount:
                    print('not enough items to apply promotion:', promotion)
                    continue
                promotion_trigger_count, _ = divmod(
                    actual_amount, qualifying_amount)
                how_many_times_promotion_can_be_applied, _ = divmod(
                    items_in_basket, free_item_amount
                )
                how_many_times_promotion_applies = min(
                    promotion_trigger_count,
                    how_many_times_promotion_can_be_applied
                )
                free_items_to_deduct = (
                    how_many_times_promotion_applies * free_item_amount)
                print('Deducting free items:', free_items_to_deduct, sku_free_item)
                print('updated_basket:', updated_basket)
                if sku_free_item in updated_basket.keys():
                    print('updating basket')
                    updated_basket[sku_free_item]['count'] -= free_items_to_deduct  # noqa

        return updated_basket

    def has_special_offer(self, sku: str) -> bool:
        print('has special offer')
        is_in_special_offers = sku in SPECIAL_OFFERS
        if not is_in_special_offers:
            return False
        amounts_qualifying = [
            offer['amount'] for offer in SPECIAL_OFFERS[sku]]

        amount_qualifies = any(
            self.basket[sku]['count'] >= amount for amount in amounts_qualifying)  # noqa
        if not amount_qualifies:
            return False
        return True

    def calculate_with_special_offer(self, sku: str) -> int:
        special_offers = SPECIAL_OFFERS[sku]
        if len(special_offers) == 1:
            special_offer = special_offers[0]
            total_with_offer, remaining_count = self.one_special_offer(
                sku, special_offer)
            remaining_total = self.reminder_no_discount(sku, remaining_count)
            total = total_with_offer + remaining_total
            print('calculate_with_special_offer:', total)
            return total

        # order special offers by amount descending
        special_offers_sorted = sorted(
            special_offers, key=lambda x: x['amount'], reverse=True)
        total = 0
        item_count = self.basket[sku]['count']
        print('item count:', item_count)
        for offer in special_offers_sorted:
            print('offer:', offer)
            if item_count == 0:
                break
            elif item_count < offer['amount']:
                continue
            else:
                total_with_offer, reminder_items = self.one_special_offer(
                    sku, offer)
                item_count = reminder_items
                print('remaining count:', item_count)
                total += total_with_offer
        total += self.reminder_no_discount(sku, item_count)
        return total

    def one_special_offer(self, sku: str, special_offer: dict) -> int:
        # how many sets of products could qualify for the special offer
        product_count = self.basket[sku]['count']
        offer_count, reminder_items = divmod(
            product_count, special_offer['amount']
        )
        print('offer count:', offer_count)
        print('remaining count:', reminder_items)
        total_with_offer = offer_count * special_offer['price']
        print('total with offer:', total_with_offer)
        already_calculated = product_count - reminder_items
        return total_with_offer, reminder_items

    def reminder_no_discount(self, sku: str, count: int = 0) -> int:
        # if no discount, return the total price
        print('reminder no discount')
        price = self.basket[sku]['price']
        if not count:
            count = self.basket[sku]['count']
        return price * count

    def calculate_total(self) -> int:
        total = 0
        for sku in self.unique_skus:
            if self.has_special_offer(sku):
                total += self.calculate_with_special_offer(sku)
            else:
                total += self.reminder_no_discount(sku)
        return total








