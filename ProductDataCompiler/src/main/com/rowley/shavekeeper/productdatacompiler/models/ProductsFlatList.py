import json
from ProductConsolidator import ProductConsolidator


class ProductsFlatList:

    def __init__(self, product_consolidator=ProductConsolidator):
        self.pre_shaves = []
        self.soaps = []
        self.brushes = []
        self.razors = []
        self.blades = []
        self.post_shaves = []
        self.after_shaves = []
        self.__flatten_consolidator(product_consolidator)

    def __add_map_to_tuple(self, product_map, tuple):
        for brand in product_map:
            for model in brand:
                tuple.append(model)

    def __flatten_consolidator(self, product_consolidator=ProductConsolidator):
        self.__add_map_to_tuple(product_consolidator.pre_shaves, self.pre_shaves)
        self.__add_map_to_tuple(product_consolidator.soaps, self.soaps)
        self.__add_map_to_tuple(product_consolidator.brushes, self.brushes)
        self.__add_map_to_tuple(product_consolidator.razors, self.razors)
        self.__add_map_to_tuple(product_consolidator.blades, self.blades)
        self.__add_map_to_tuple(product_consolidator.post_shaves, self.post_shaves)
        self.__add_map_to_tuple(product_consolidator.after_shaves, self.after_shaves)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def from_JSON(self, json_string):
        return json.loads(self, json_string, cls=ProductsFlatList.__class__)
