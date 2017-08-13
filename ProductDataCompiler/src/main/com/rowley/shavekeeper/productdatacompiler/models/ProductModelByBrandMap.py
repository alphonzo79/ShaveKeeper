import json

from ProductModels import ItemBase


class ProductModelByBrandMap:
    """This class is meant to capture all models by brand, regardless of product type, for the
    purpose of manually going through by a human to update the model name and ultimately
    de-duplicate some products that we can't do easily during the screenscrape."""

    def __init__(self):
        self.brands = {}

    @classmethod
    def add_item(self, item):
        if item.brand not in self.brands:
            self.brands[item.brand] = {}

        if item.model not in self.brands[item.brand]:
            self.brands[item.brand][item.model] = ItemBase(item.brand, item.model)

    @classmethod
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))

    def from_JSON(self, json_string):
        return json.loads(self, json_string, cls=ProductModelByBrandMap.__class__)
