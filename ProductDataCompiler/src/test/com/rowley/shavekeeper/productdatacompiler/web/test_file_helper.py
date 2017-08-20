from unittest import TestCase

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import AfterShave
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import save_file, load_file, \
    load_consolidator_and_reconciler


class TestFileHelper(TestCase):
    def test_save_file(self):
        products = ProductConsolidator()
        products.add_after_shave(AfterShave("brand", "model"))
        save_file(products, filename="TestFile")
        #manually verify :shrug:

    def test_load_file_doesnt_exist(self):
        products = load_file(filename="NonExistent")
        self.assertTrue(products is None)

    def test_load_file_exists(self):
        reference = ProductConsolidator()
        reference.add_after_shave(AfterShave("brand", "model"))
        products = load_file("TestFile")
        self.assertEqual(reference.to_json(), products)

    def test_load_consolidator_and_reconciler(self):
        consolidator, reconciler = load_consolidator_and_reconciler()
        self.assertIsNotNone(consolidator)
        self.assertIsNotNone(reconciler)
