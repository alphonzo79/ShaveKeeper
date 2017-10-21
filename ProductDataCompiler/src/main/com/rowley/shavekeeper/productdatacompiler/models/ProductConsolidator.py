import json
import ProductModels


class ProductConsolidator:

    def __init__(self, pre_shaves=None, soaps=None, brushes=None,
                 razors=None, blades=None, post_shaves=None, after_shaves=None):
        if pre_shaves is None:
            pre_shaves = {}
        if soaps is None:
            soaps = {}
        if brushes is None:
            brushes = {}
        if razors is None:
            razors = {}
        if blades is None:
            blades = {}
        if post_shaves is None:
            post_shaves = {}
        if after_shaves is None:
            after_shaves = {}
        self.pre_shaves = pre_shaves
        self.soaps = soaps
        self.brushes = brushes
        self.razors = razors
        self.blades = blades
        self.post_shaves = post_shaves
        self.after_shaves = after_shaves

    def __add_item_to_map__(self, item, product_map):
        """Internal method to abstract adding a new item to an existing map. To avoid
        duplication we first check whether a brand, then a model already exists and skips
        adding the item."""
        brand = ""
        model = ""
        try:
            brand = item.brand
        except AttributeError:
            brand = item["brand"]

        try:
            model = item.model
        except AttributeError:
            model = item["model"]

        if brand not in product_map:
            product_map[brand] = {}
        if model not in product_map[brand]:
            product_map[brand][model] = item

    def add_pre_shave(self, pre_shave=ProductModels.PostShave):
        """Add a PreShave to the ProductConsolidator. If this preshave, determined by
        brand/model, already exists it will not be added"""
        self.__add_item_to_map__(pre_shave, self.pre_shaves)

    def add_soap(self, soap=ProductModels.Soap):
        """Add a Soap to the ProductConsolidator. If this soap, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(soap, self.soaps)

    def add_brush(self, brush=ProductModels.Brush):
        """Add a Brush to the ProductConsolidator. If this brush, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(brush, self.brushes)

    def add_razor(self, razor=ProductModels.Razor):
        """Add a Razor to the ProductConsolidator. If this razor, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(razor, self.razors)

    def add_blade(self, blade=ProductModels.Blade):
        """Add a Blade to the ProductConsolidator. If this blade, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(blade, self.blades)

    def add_post_shave(self, post_shave=ProductModels.PostShave):
        """Add a PostShave to the ProductConsolidator. If this post_shave, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(post_shave, self.post_shaves)

    def add_after_shave(self, after_shave=ProductModels.AfterShave):
        """Add a AfterShave to the ProductConsolidator. If this after_shave, determined by brand/model,
        already exists it will not be added"""
        self.__add_item_to_map__(after_shave, self.after_shaves)

    def __eq__(self, other):
        if self is other:
            return True

        if type(self) is not type(other):
            return False

        #Take the easy way out since I don't know how to do this better with a specific type down in there sometimes
        # showing up as a bare dict
        return cmp(self.to_json(), other.to_json()) is 0

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def payload_hook(dct):
        return ProductConsolidator(dct["pre_shaves"], dct["soaps"], dct["brushes"],
                                   dct["razors"], dct["blades"], dct["post_shaves"], dct["after_shaves"])

    @staticmethod
    def from_json(json_string):
        return ProductConsolidator.payload_hook(json.loads(json_string, object_pairs_hook=dict))
