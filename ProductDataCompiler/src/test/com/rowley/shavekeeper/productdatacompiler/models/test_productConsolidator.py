from unittest import TestCase
from mock import MagicMock

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import ItemBase
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Soap
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PreShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Blade
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PostShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import AfterShave


class TestProductConsolidator(TestCase):

    def test_add_item_to_map(self):
        product_consolidator = ProductConsolidator()
        brand = "I'm a brand"
        model = "I'm a model"
        item = ItemBase(brand, model)
        product_consolidator.__add_item_to_map__(item, product_consolidator.pre_shaves)
        self.assertTrue(item.brand in product_consolidator.pre_shaves)
        self.assertTrue(item.model in product_consolidator.pre_shaves[item.brand])
        self.assertEqual(item, product_consolidator.pre_shaves[item.brand][item.model])

    def test_add_item_to_map_only_adds_one(self):
        product_consolidator = ProductConsolidator()
        brand = "I'm a brand"
        model = "I'm a model"
        item = ItemBase(brand, model)
        product_consolidator.__add_item_to_map__(item, product_consolidator.pre_shaves)

        item_two = ItemBase(brand, model)

        product_consolidator.__add_item_to_map__(item_two, product_consolidator.pre_shaves)
        self.assertTrue(item.brand in product_consolidator.pre_shaves)
        self.assertTrue(item.model in product_consolidator.pre_shaves[item.brand])
        self.assertEqual(item, product_consolidator.pre_shaves[item.brand][item.model])

    def set_up_mock(self):
        product_consolidator = ProductConsolidator()
        product_consolidator.__add_item_to_map__ = MagicMock(return_value=True)
        return product_consolidator

    def test_add_pre_shave(self):
        product_consolidator = self.set_up_mock()
        pre_shave = PreShave
        product_consolidator.add_pre_shave(pre_shave)
        product_consolidator.__add_item_to_map__.assert_called_with(pre_shave, product_consolidator.pre_shaves)

    def test_add_soap(self):
        product_consolidator = self.set_up_mock()
        soap = Soap
        product_consolidator.add_soap(soap)
        product_consolidator.__add_item_to_map__.assert_called_with(soap, product_consolidator.soaps)

    def test_add_brush(self):
        product_consolidator = self.set_up_mock()
        brush = Brush
        product_consolidator.add_brush(brush)
        product_consolidator.__add_item_to_map__.assert_called_with(brush, product_consolidator.brushes)

    def test_add_razor(self):
        product_consolidator = self.set_up_mock()
        razor = Razor
        product_consolidator.add_razor(razor)
        product_consolidator.__add_item_to_map__.assert_called_with(razor, product_consolidator.razors)

    def test_add_blade(self):
        product_consolidator = self.set_up_mock()
        blade = Blade
        product_consolidator.add_blade(blade)
        product_consolidator.__add_item_to_map__.assert_called_with(blade, product_consolidator.blades)

    def test_add_post_shave(self):
        product_consolidator = self.set_up_mock()
        post_shave = PostShave
        product_consolidator.add_post_shave(post_shave)
        product_consolidator.__add_item_to_map__.assert_called_with(post_shave, product_consolidator.post_shaves)

    def test_add_after_shave(self):
        product_consolidator = self.set_up_mock()
        after_shave = AfterShave
        product_consolidator.add_after_shave(after_shave)
        product_consolidator.__add_item_to_map__.assert_called_with(after_shave, product_consolidator.after_shaves)

    def test_eq_same_instance(self):
        product_consolidator = ProductConsolidator()
        self.assertEqual(product_consolidator, product_consolidator)

    def test_eq_different_types(self):
        self.assertNotEqual(ProductConsolidator(), Brush())

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

    product_consolidator_json_string = '{"after_shaves":{"AfterShave 1 brand":{"AfterShave 1 model":{"brand":"' \
                                       'AfterShave 1 brand","model":"AfterShave 1 model"}}},"blades":{"Blade 1 brand"' \
                                       ':{"Blade 1 model":{"brand":"Blade 1 brand","model":"Blade 1 model"},"Blade 2' \
                                       ' model":{"brand":"Blade 1 brand","model":"Blade 2 model"},"Blade 5 model":{' \
                                       '"brand":"Blade 1 brand","model":"Blade 5 model"}},"Blade 3 brand":{"Blade 3' \
                                       ' model":{"brand":"Blade 3 brand","model":"Blade 3 model"}},"Blade 4 brand":{' \
                                       '"Blade 4 model":{"brand":"Blade 4 brand","model":"Blade 4 model"}}},"brushes"' \
                                       ':{"brush brand":{"brush model":{"brand":"brush brand","fiber":"Boar",' \
                                       '"knot_size":"25mm","model":"brush model"}}},"post_shaves":{"Post Shave 1 ' \
                                       'brand":{"Post Shave 1 model":{"brand":"Post Shave 1 brand","model":"Post ' \
                                       'Shave 1 model"}},"Post Shave 2 brand":{"Post Shave 2 model":{"brand":"Post ' \
                                       'Shave 2 brand","model":"Post Shave 2 model"}}},"pre_shaves":{"Preshave 1 ' \
                                       'brand":{"Preshave 1 model":{"brand":"Preshave 1 brand","model":"Preshave 1 ' \
                                       'model"}},"Preshave 2 brand":{"Preshave 2 model":{"brand":"Preshave 2 brand",' \
                                       '"model":"Preshave 2 model"},"Preshave 3 model":{"brand":"Preshave 2 brand",' \
                                       '"model":"Preshave 3 model"}}},"razors":{"Razor 1 brand":{"Razor 1 model":{' \
                                       '"brand":"Razor 1 brand","is_adjustable":false,"model":"Razor 1 model","' \
                                       'razor_type":"DE","uses_blade":true}},"Razor 2 brand":{"Razor 2 model":{' \
                                       '"brand":"Razor 2 brand","is_adjustable":false,"model":"Razor 2 model",' \
                                       '"razor_type":"Straight Blade","uses_blade":false}}},"soaps":{"Soap 1 brand":' \
                                       '{"Soap 1 model":{"brand":"Soap 1 brand","model":"Soap 1 model"},"Soap 2 ' \
                                       'model":{"brand":"Soap 1 brand","model":"Soap 2 model"},"Soap 3 model":{' \
                                       '"brand":"Soap 1 brand","model":"Soap 3 model"}}}}'

    def test_eq_same_instance(self):
        product_consolidator = ProductConsolidator()
        self.assertEqual(product_consolidator, product_consolidator)

    def test_eq_different_types(self):
        self.assertNotEqual(ProductConsolidator(), Brush())

    def test_eq_equivalent_instances(self):
        compiler1 = self.create_test_product_consolidator()
        compiler2 = self.create_test_product_consolidator()
        self.assertEqual(compiler1, compiler2)

    def test_eq_non_equivalent_instances(self):
        compiler1 = self.create_test_product_consolidator()
        compiler2 = self.create_test_product_consolidator()
        compiler2.pre_shaves = {}
        self.assertNotEqual(compiler1, compiler2)

    def test_to_JSON(self):
        product_consolidator = self.create_test_product_consolidator()
        json = product_consolidator.to_json()
        self.assertEquals(json, self.product_consolidator_json_string)

    def test_from_JSON(self):
        product_consolidator = ProductConsolidator.from_json(self.product_consolidator_json_string)
        reference_consolidator = self.create_test_product_consolidator()
        self.assertEquals(product_consolidator, reference_consolidator)
