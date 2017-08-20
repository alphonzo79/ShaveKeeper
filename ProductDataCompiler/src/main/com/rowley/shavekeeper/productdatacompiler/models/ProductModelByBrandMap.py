import json

from ProductModels import ItemBase


class ProductModelByBrandMap:
    """This class is meant to capture all models by brand, regardless of product type, for the
    purpose of manually going through by a human to update the model name and ultimately
    de-duplicate some products that we can't do easily during the screenscrape."""

    def __init__(self, product_consolidator=None, brands=None):
        if brands is None:
            brands = {}
        self.brands = brands
        if product_consolidator is not None:
            self.__flatten_consolidator__(product_consolidator)

    def __add_item__(self, item):
        if item.brand not in self.brands:
            self.brands[item.brand] = {}

        if item.model not in self.brands[item.brand]:
            self.brands[item.brand][item.model] = ItemBase(item.brand, item.model)

    def __add_consolidator_map_to_simple_map__(self, consolidator_map):
        for brand in consolidator_map:
            for model in consolidator_map[brand]:
                self.__add_item__(consolidator_map[brand][model])

    def __flatten_consolidator__(self, product_consolidator):
        self.__add_consolidator_map_to_simple_map__(product_consolidator.pre_shaves)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.soaps)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.brushes)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.razors)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.blades)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.post_shaves)
        self.__add_consolidator_map_to_simple_map__(product_consolidator.after_shaves)

    def __eq__(self, other):
        if self is other:
            return True

        if type(self) is not type(other):
            return False

        # Take the easy way out since I don't know how to do this better with a specific type down in there sometimes
        # showing up as a bare dict
        return cmp(self.to_json(), other.to_json()) is 0

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def payload_hook(dct):
        return ProductModelByBrandMap(brands=dct["brands"])

    @staticmethod
    def from_json(json_string):
        return ProductModelByBrandMap.payload_hook(json.loads(json_string, object_pairs_hook=dict))
