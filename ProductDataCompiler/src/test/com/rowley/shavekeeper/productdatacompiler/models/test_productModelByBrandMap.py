from unittest import TestCase
from mock import MagicMock, call

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModelByBrandMap import ProductModelByBrandMap
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Soap
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PreShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Blade
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PostShave
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import AfterShave


class TestProductModelByBrandMap(TestCase):
        
    brand_one = "Brand One"
    brand_two = "Brand Two"

    def create_test_product_consolidator(self):
        product_consolidator = ProductConsolidator()

        pre_shave_1 = PreShave(self.brand_one, "Preshave 1 model")
        product_consolidator.add_pre_shave(pre_shave_1)
        pre_shave_2 = PreShave(self.brand_two, "Preshave 2 model")
        product_consolidator.add_pre_shave(pre_shave_2)
        pre_shave_3 = PreShave(self.brand_two, "Preshave 3 model")
        product_consolidator.add_pre_shave(pre_shave_3)

        soap_1 = Soap(self.brand_one, "Soap 1 model")
        product_consolidator.add_soap(soap_1)
        soap_2 = Soap(self.brand_one, "Soap 2 model")
        product_consolidator.add_soap(soap_2)
        soap_3 = Soap(self.brand_one, "Soap 3 model")
        product_consolidator.add_soap(soap_3)

        brush = Brush(self.brand_one, "brush model", "25mm", "Boar")
        product_consolidator.add_brush(brush)

        razor_1 = Razor(self.brand_one, "Razor 1 model", "DE", True, False)
        product_consolidator.add_razor(razor_1)
        razor_2 = Razor(self.brand_two, "Razor 2 model", "Straight Blade", False, False)
        product_consolidator.add_razor(razor_2)

        blade_1 = Blade(self.brand_one, "Blade 1 model")
        product_consolidator.add_blade(blade_1)
        blade_2 = Blade(self.brand_one, "Blade 2 model")
        product_consolidator.add_blade(blade_2)
        blade_3 = Blade(self.brand_two, "Blade 3 model")
        product_consolidator.add_blade(blade_3)
        blade_4 = Blade(self.brand_two, "Blade 4 model")
        product_consolidator.add_blade(blade_4)
        blade_5 = Blade(self.brand_one, "Blade 5 model")
        product_consolidator.add_blade(blade_5)

        post_shave_1 = PostShave(self.brand_one, "Post Shave 1 model")
        product_consolidator.add_post_shave(post_shave_1)
        post_shave_2 = PostShave(self.brand_two, "Post Shave 2 model")
        product_consolidator.add_post_shave(post_shave_2)

        after_shave_1 = AfterShave(self.brand_one, "AfterShave 1 model")
        product_consolidator.add_after_shave(after_shave_1)

        return product_consolidator

    def create_test_product_by_brand_map(self):
        return ProductModelByBrandMap(product_consolidator=self.create_test_product_consolidator())

    def test_add_item(self):
        product_consolidator = self.create_test_product_consolidator()
        product_by_brand_map = ProductModelByBrandMap()
        for brand in product_consolidator.pre_shaves:
            for model in product_consolidator.pre_shaves[brand]:
                product_by_brand_map.__add_item__(product_consolidator.pre_shaves[brand][model])

        self.assertTrue(self.brand_one in product_by_brand_map.brands)
        self.assertTrue("Preshave 1 model" in product_by_brand_map.brands["Brand One"])
        self.assertTrue(self.brand_two in product_by_brand_map.brands)
        self.assertTrue("Preshave 2 model" in product_by_brand_map.brands["Brand Two"])
        self.assertTrue("Preshave 3 model" in product_by_brand_map.brands["Brand Two"])

    def test_add_consolidator_map_to_simple_map(self):
        product_consolidator = self.create_test_product_consolidator()
        product_by_brand_map = ProductModelByBrandMap()
        product_by_brand_map.__add_item__ = MagicMock()

        product_by_brand_map.__add_consolidator_map_to_simple_map__(product_consolidator.blades)
        product_by_brand_map.__add_item__.assert_has_calls([
            call(product_consolidator.blades["Brand One"]["Blade 1 model"]),
            call(product_consolidator.blades["Brand One"]["Blade 2 model"]),
            call(product_consolidator.blades["Brand Two"]["Blade 3 model"]),
            call(product_consolidator.blades["Brand Two"]["Blade 4 model"]),
            call(product_consolidator.blades["Brand One"]["Blade 5 model"])], True)

    def test_flatten_consolidator(self):
        product_consolidator = self.create_test_product_consolidator()
        product_by_brand_map = ProductModelByBrandMap()
        product_by_brand_map.__add_consolidator_map_to_simple_map__ = MagicMock()

        product_by_brand_map.__flatten_consolidator__(product_consolidator)
        product_by_brand_map.__add_consolidator_map_to_simple_map__.assert_has_calls([
            call(product_consolidator.pre_shaves),
            call(product_consolidator.soaps),
            call(product_consolidator.brushes),
            call(product_consolidator.razors),
            call(product_consolidator.blades),
            call(product_consolidator.post_shaves),
            call(product_consolidator.after_shaves)], True)

    product_by_brand_map_json = '{"brands":{"Brand One":{"AfterShave 1 model":{"brand":"Brand One","model":' \
                                '"AfterShave 1 model"},"Blade 1 model":{"brand":"Brand One","model":"Blade 1 model"},' \
                                '"Blade 2 model":{"brand":"Brand One","model":"Blade 2 model"},"Blade 5 model":{' \
                                '"brand":"Brand One","model":"Blade 5 model"},"Post Shave 1 model":{"brand":' \
                                '"Brand One","model":"Post Shave 1 model"},"Preshave 1 model":{"brand":"Brand One",' \
                                '"model":"Preshave 1 model"},"Razor 1 model":{"brand":"Brand One","model":' \
                                '"Razor 1 model"},"Soap 1 model":{"brand":"Brand One","model":"Soap 1 model"},' \
                                '"Soap 2 model":{"brand":"Brand One","model":"Soap 2 model"},"Soap 3 model":{"brand":' \
                                '"Brand One","model":"Soap 3 model"},"brush model":{"brand":"Brand One","model":' \
                                '"brush model"}},"Brand Two":{"Blade 3 model":{"brand":"Brand Two","model":' \
                                '"Blade 3 model"},"Blade 4 model":{"brand":"Brand Two","model":"Blade 4 model"},' \
                                '"Post Shave 2 model":{"brand":"Brand Two","model":"Post Shave 2 model"},' \
                                '"Preshave 2 model":{"brand":"Brand Two","model":"Preshave 2 model"},' \
                                '"Preshave 3 model":{"brand":"Brand Two","model":"Preshave 3 model"},"Razor 2 model":' \
                                '{"brand":"Brand Two","model":"Razor 2 model"}}}}'

    def test_eq_same_instance(self):
        product_by_brand_map = ProductModelByBrandMap()
        self.assertEqual(product_by_brand_map, product_by_brand_map)

    def test_eq_different_types(self):
        self.assertNotEqual(ProductModelByBrandMap(), Brush())

    def test_eq_equivalent_instances(self):
        simple_map1 = self.create_test_product_by_brand_map()
        simple_map2 = self.create_test_product_by_brand_map()
        self.assertEqual(simple_map1, simple_map2)

    def test_eq_non_equivalent_instances(self):
        simple_map1 = self.create_test_product_by_brand_map()
        simple_map2 = self.create_test_product_by_brand_map()
        simple_map2.brands[0] = {}
        self.assertNotEqual(simple_map1, simple_map2)

    def test_to_json(self):
        product_consolidator = self.create_test_product_consolidator()
        product_by_brand_map = ProductModelByBrandMap()
        product_by_brand_map.__flatten_consolidator__(product_consolidator)
        self.assertEqual(self.product_by_brand_map_json, product_by_brand_map.to_json())

    def test_from_json(self):
        product_by_brand_map = ProductModelByBrandMap.from_json(self.product_by_brand_map_json)
        reference_map = self.create_test_product_by_brand_map()
        self.assertEquals(product_by_brand_map, reference_map)
