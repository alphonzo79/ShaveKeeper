import json
import ProductModels


class ProductConsolidator:

    def __init__(self):
        pass

    pre_shaves = {}
    soaps = {}
    brushes = {}
    razors = {}
    blades = {}
    post_shaves = {}
    after_shaves = {}

    @classmethod
    def __add_item_to_map__(self, item, product_map):
        """Internal method to abstract adding a new item to an existing map. To avoid
        duplication we first check whether a brand, then a model already exists and skips
        adding the item."""
        if item.brand not in product_map:
            product_map[item.brand] = {}
        if item.model not in product_map[item.brand]:
            product_map[item.brand][item.model] = item

    @classmethod
    def add_pre_shave(self, pre_shave=ProductModels.PostShave):
        """Add a PreShave to the ProductConsolidator. If this preshave, determined by
        brand/model, already exists it will not be added"""
        self.__add_item_to_map__(pre_shave, self.pre_shaves)

    @classmethod
    def add_soap(self, soap=ProductModels.Soap):
        """Add a Soap to the ProductConsolidator. If this soap, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(soap, self.soaps)

    @classmethod
    def add_brush(self, brush=ProductModels.Brush):
        """Add a Brush to the ProductConsolidator. If this brush, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(brush, self.brushes)

    @classmethod
    def add_razor(self, razor=ProductModels.Razor):
        """Add a Razor to the ProductConsolidator. If this razor, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(razor, self.razors)

    @classmethod
    def add_blade(self, blade=ProductModels.Blade):
        """Add a Blade to the ProductConsolidator. If this blade, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(blade, self.blades)

    @classmethod
    def add_post_shave(self, post_shave=ProductModels.PostShave):
        """Add a PostShave to the ProductConsolidator. If this post_shave, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(post_shave, self.post_shaves)

    @classmethod
    def add_after_shave(self, after_shave=ProductModels.AfterShave):
        """Add a AfterShave to the ProductConsolidator. If this after_shave, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(after_shave, self.after_shaves)

    @classmethod
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def from_json(json_string):
        return json.loads(json_string)
