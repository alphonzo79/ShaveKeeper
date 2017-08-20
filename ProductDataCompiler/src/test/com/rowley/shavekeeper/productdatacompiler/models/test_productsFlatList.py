from unittest import TestCase
from mock import MagicMock
from mock import call

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductsFlatList import ProductsFlatList
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import ItemBase
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Soap
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PreShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Blade
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PostShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import AfterShave


class TestProductsFlatList(TestCase):

    def create_test_product_consolidator(self):
        product_consolidator = ProductConsolidator()

        pre_shave_1 = PreShave("Preshave 1 brand", "Preshave 1 model")
        product_consolidator.add_pre_shave(pre_shave_1)
        pre_shave_2 = PreShave("Preshave 2 brand", "Preshave 2 model")
        product_consolidator.add_pre_shave(pre_shave_2)
        pre_shave_3 = PreShave("Preshave 2 brand", "Preshave 3 model")
        product_consolidator.add_pre_shave(pre_shave_3)

        soap_1 = Soap("Soap 1 brand", "Soap 1 model")
        product_consolidator.add_soap(soap_1)
        soap_2 = Soap("Soap 1 brand", "Soap 2 model")
        product_consolidator.add_soap(soap_2)
        soap_3 = Soap("Soap 1 brand", "Soap 3 model")
        product_consolidator.add_soap(soap_3)

        brush = Brush("brush brand", "brush model", "25mm", "Boar")
        product_consolidator.add_brush(brush)

        razor_1 = Razor("Razor 1 brand", "Razor 1 model", "DE", True, False)
        product_consolidator.add_razor(razor_1)
        razor_2 = Razor("Razor 2 brand", "Razor 2 model", "Straight Blade", False, False)
        product_consolidator.add_razor(razor_2)

        blade_1 = Blade("Blade 1 brand", "Blade 1 model")
        product_consolidator.add_blade(blade_1)
        blade_2 = Blade("Blade 1 brand", "Blade 2 model")
        product_consolidator.add_blade(blade_2)
        blade_3 = Blade("Blade 3 brand", "Blade 3 model")
        product_consolidator.add_blade(blade_3)
        blade_4 = Blade("Blade 4 brand", "Blade 4 model")
        product_consolidator.add_blade(blade_4)
        blade_5 = Blade("Blade 1 brand", "Blade 5 model")
        product_consolidator.add_blade(blade_5)

        post_shave_1 = PostShave("Post Shave 1 brand", "Post Shave 1 model")
        product_consolidator.add_post_shave(post_shave_1)
        post_shave_2 = PostShave("Post Shave 2 brand", "Post Shave 2 model")
        product_consolidator.add_post_shave(post_shave_2)

        after_shave_1 = AfterShave("AfterShave 1 brand", "AfterShave 1 model")
        product_consolidator.add_after_shave(after_shave_1)

        return product_consolidator

    def test_add_map_to_tuple(self):
        product_flat_list = ProductsFlatList()
        brand_one = "brand One"
        brand_two = "brand Two"
        model_one = "model One"
        model_two = "model Two"
        item_one = ItemBase(brand_one, model_one)
        item_two = ItemBase(brand_one, model_two)
        item_three = ItemBase(brand_two, model_one)
        item_four = ItemBase(brand_two, model_two)
        product_map = {brand_one: {model_one: item_one, model_two: item_two},
                       brand_two: {model_one: item_three, model_two: item_four}}
        product_flat_list.__add_map_to_tuple__(product_map, product_flat_list.pre_shaves)
        self.assertTrue(item_one in product_flat_list.pre_shaves)
        self.assertTrue(item_two in product_flat_list.pre_shaves)
        self.assertTrue(item_three in product_flat_list.pre_shaves)
        self.assertTrue(item_four in product_flat_list.pre_shaves)

    def test_flatten_consolidator(self):
        product_consolidator = self.create_test_product_consolidator()
        products_flat_list = ProductsFlatList()
        products_flat_list.__add_map_to_tuple__ = MagicMock(return_value=None)
        products_flat_list.__flatten_consolidator__(product_consolidator)

        products_flat_list.__add_map_to_tuple__.assert_has_calls(
            [call(product_consolidator.pre_shaves, products_flat_list.pre_shaves),
                call(product_consolidator.soaps, products_flat_list.soaps),
                call(product_consolidator.brushes, products_flat_list.brushes),
                call(product_consolidator.razors, products_flat_list.razors),
                call(product_consolidator.blades, products_flat_list.blades),
                call(product_consolidator.post_shaves, products_flat_list.post_shaves),
                call(product_consolidator.after_shaves, products_flat_list.after_shaves)], True)

    def test_initialize_with_consolidator(self):
        product_consolidator = self.create_test_product_consolidator()
        products_flat_list = ProductsFlatList(product_consolidator)
        self.assertEqual(len(products_flat_list.pre_shaves), 3)
        self.assertEqual(len(products_flat_list.soaps), 3)
        self.assertEqual(len(products_flat_list.brushes), 1)
        self.assertEqual(len(products_flat_list.razors), 2)
        self.assertEqual(len(products_flat_list.blades), 5)
        self.assertEqual(len(products_flat_list.post_shaves), 2)
        self.assertEqual(len(products_flat_list.after_shaves), 1)

    product_flat_list_json = '{"after_shaves":[{"brand":"AfterShave 1 brand","model":"AfterShave 1 model"}],"blades":' \
                             '[{"brand":"Blade 4 brand","model":"Blade 4 model"},{"brand":"Blade 1 brand","model":' \
                             '"Blade 1 model"},{"brand":"Blade 1 brand","model":"Blade 5 model"},{"brand":"Blade 1 ' \
                             'brand","model":"Blade 2 model"},{"brand":"Blade 3 brand","model":"Blade 3 model"}],' \
                             '"brushes":[{"brand":"brush brand","fiber":"Boar","knot_size":"25mm","model":"brush ' \
                             'model"}],"post_shaves":[{"brand":"Post Shave 2 brand","model":"Post Shave 2 model"},{' \
                             '"brand":"Post Shave 1 brand","model":"Post Shave 1 model"}],"pre_shaves":[{"brand":' \
                             '"Preshave 2 brand","model":"Preshave 3 model"},{"brand":"Preshave 2 brand","model":' \
                             '"Preshave 2 model"},{"brand":"Preshave 1 brand","model":"Preshave 1 model"}],"razors":[' \
                             '{"brand":"Razor 2 brand","is_adjustable":false,"model":"Razor 2 model","razor_type":' \
                             '"Straight Blade","uses_blade":false},{"brand":"Razor 1 brand","is_adjustable":false,' \
                             '"model":"Razor 1 model","razor_type":"DE","uses_blade":true}],"soaps":[{"brand":"Soap ' \
                             '1 brand","model":"Soap 3 model"},{"brand":"Soap 1 brand","model":"Soap 1 model"},{' \
                             '"brand":"Soap 1 brand","model":"Soap 2 model"}]}'

    def test_to_json(self):
        product_consolidator = self.create_test_product_consolidator()
        product_flat_list = ProductsFlatList(product_consolidator)
        self.assertEqual(self.product_flat_list_json, product_flat_list.to_json())
