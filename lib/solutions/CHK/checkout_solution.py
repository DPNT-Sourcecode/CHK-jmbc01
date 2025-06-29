
BASIC_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
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
    'F': [{
        'qualifying_amount': 2,
        'free_item': 'F',
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
        print(f"Updated basket: {updated_basket}")  # noqa
        return updated_basket

    def _update_basket_with_free_items(self, basket) -> dict:
        updated_basket = basket.copy()
        for sku, item in basket.items():
            if sku not in FREE_ITEMS_PROMOTIONS:
                continue
            free_item_promotions = FREE_ITEMS_PROMOTIONS[sku]
            for promotion in free_item_promotions:
                free_item_amount = promotion.get('free_item_amount', 0)
                sku_free_item = promotion['free_item']
                items_in_basket = updated_basket.get(
                    sku_free_item, {}).get('count', 0)
                not_enough_in_basket_to_apply_promotion = (
                    items_in_basket < free_item_amount)
                if not_enough_in_basket_to_apply_promotion:
                    continue
                qualifying_amount = promotion['qualifying_amount']
                actual_amount = item['count']
                if sku_free_item == sku:
                    if actual_amount <= qualifying_amount:
                        # if the free item is the same as the qualifying item
                        # we only apply promotion if the amount is greater
                        # than the qualifying amount
                        continue
                if actual_amount < qualifying_amount:
                    continue
                promotion_trigger_count, _ = divmod(
                    actual_amount, qualifying_amount)
                print(f"Promotion trigger count for {sku}: {promotion_trigger_count}")
                if sku_free_item == sku:
                    reduced_amount = self._apply_reduction_rounds_same_product(
                        triggers=promotion_trigger_count,
                        amount_remaining=items_in_basket,
                        free_item_amount=free_item_amount,
                        qualifying_amount=qualifying_amount
                    )
                else:
                    reduced_amount = self._apply_reduction_rounds(
                        triggers=promotion_trigger_count,
                        amount_remaining=items_in_basket,
                        free_item_amount=free_item_amount
                    )
                print(f"Reduced amount for {sku_free_item}: {reduced_amount}")  # noqa
                if sku_free_item in updated_basket.keys():
                    updated_basket[sku_free_item]['count'] = reduced_amount  # noqa

        return updated_basket

    def _apply_reduction_rounds(
            self, *,
            triggers: int,
            amount_remaining: int,
            free_item_amount: int) -> int:
        updated_amount = amount_remaining

        if updated_amount < 0:
            raise ValueError(
                f"Amount remaining cannot be negative: {amount_remaining}"
            )
        triggers_run = triggers
        for _ in range(triggers):
            print('inside forlooptriggers_run:', triggers_run)  # noqa
            if updated_amount == 0:
                print('Updated amount is 0, returning 0')
                return 0
            if triggers_run == 0:
                print('No more triggers to run, returning updated amount:', updated_amount)
                return updated_amount
            if updated_amount < free_item_amount:
                print('Updated amount is less than free item amount, returning updated amount:', updated_amount)
                return updated_amount
            updated_amount -= free_item_amount
            print(f"Updated amount after reduction: {updated_amount}")
            triggers_run -= 1
        print('triggers_run:', triggers_run)  # noqa
        return updated_amount


    def _apply_reduction_rounds_same_product(
            self, *,
            triggers: int,
            amount_remaining: int,
            free_item_amount: int,
            qualifying_amount: int) -> int:
        print('RUNNING FOR SAME PRODUCT')
        updated_amount = amount_remaining
        processed_for_promotion = amount_remaining

        if updated_amount < 0:
            raise ValueError(
                f"Amount remaining cannot be negative: {amount_remaining}"
            )
        triggers_run = triggers
        for _ in range(triggers):
            print('inside forlooptriggers_run:', triggers_run)  # noqa
            if updated_amount == 0:
                print('Updated amount is 0, returning 0')
                return 0
            if triggers_run == 0:
                print('No more triggers to run, returning updated amount:', updated_amount)
                return updated_amount
            if processed_for_promotion <= qualifying_amount:
                print('Updated amount is less than or equal to qualifying amount, returning updated amount:', updated_amount)
                return updated_amount
            if updated_amount < free_item_amount:
                print('Updated amount is less than free item amount, returning updated amount:', updated_amount)
                return updated_amount
            updated_amount -= free_item_amount
            processed_for_promotion -= qualifying_amount - free_item_amount
            print(f"Processed for promotion: {processed_for_promotion}")  # noqa
            print(f"Updated amount after reduction: {updated_amount}")
            triggers_run -= 1
        print('triggers_run:', triggers_run)  # noqa
        return updated_amount

    def has_special_offer(self, sku: str) -> bool:
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
            total = 0
            special_offer = special_offers[0]
            total_with_offer, calculated = self.one_special_offer(
                sku, special_offer)
            total += total_with_offer
            remaining_count = self.basket[sku]['count'] - calculated
            if remaining_count:
                total += self.reminder_no_discount(sku, remaining_count)

            return total

        # order special offers by amount descending
        special_offers_sorted = sorted(
            special_offers, key=lambda x: x['amount'], reverse=True)
        total = 0
        item_count = self.basket[sku]['count']
        if item_count == 0:
            return 0
        for offer in special_offers_sorted:
            if item_count < offer['amount']:
                continue
            else:
                total_with_offer, already_calculated = self.one_special_offer(
                    sku, offer, item_count)
                item_count -= already_calculated
                total += total_with_offer
        if item_count:
            total += self.reminder_no_discount(sku, item_count)
        return total

    def one_special_offer(
            self, sku: str, special_offer: dict, item_count: int = 0) -> int:
        # how many sets of products could qualify for the special offer
        if not item_count:
            product_count = self.basket[sku]['count']
        else:
            product_count = item_count
        offer_count, reminder_items = divmod(
            product_count, special_offer['amount']
        )
        total_with_offer = offer_count * special_offer['price']
        already_calculated = product_count - reminder_items
        return total_with_offer, already_calculated

    def reminder_no_discount(self, sku: str, count: int = 0) -> int:
        # if no discount, return the total price
        price = self.basket[sku]['price']
        if not count:
            count = self.basket[sku]['count']
        total = price * count

        return total

    def calculate_total(self) -> int:
        total = 0
        for sku in self.unique_skus:
            if self.has_special_offer(sku):
                total += self.calculate_with_special_offer(sku)
            else:
                total += self.reminder_no_discount(sku)
        return total




