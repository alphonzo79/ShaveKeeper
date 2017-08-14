import json


class ProductsFlatList:

    def __init__(self, product_consolidator=None):
        self.pre_shaves = []
        self.soaps = []
        self.brushes = []
        self.razors = []
        self.blades = []
        self.post_shaves = []
        self.after_shaves = []
        if product_consolidator is not None:
            self.__flatten_consolidator__(product_consolidator)

    def __add_map_to_tuple__(self, product_map, target):
        for brand in product_map:
            for model in product_map[brand]:
                target.append(product_map[brand][model])

    def __flatten_consolidator__(self, product_consolidator):
        self.__add_map_to_tuple__(product_consolidator.pre_shaves, self.pre_shaves)
        self.__add_map_to_tuple__(product_consolidator.soaps, self.soaps)
        self.__add_map_to_tuple__(product_consolidator.brushes, self.brushes)
        self.__add_map_to_tuple__(product_consolidator.razors, self.razors)
        self.__add_map_to_tuple__(product_consolidator.blades, self.blades)
        self.__add_map_to_tuple__(product_consolidator.post_shaves, self.post_shaves)
        self.__add_map_to_tuple__(product_consolidator.after_shaves, self.after_shaves)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))
