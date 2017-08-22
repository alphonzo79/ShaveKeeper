import os

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModelByBrandMap import ProductModelByBrandMap

consolidated_products_filename = "ConsolidatedProducts"
reconciler_filename = "Reconciler"
flat_list_filename = "ProductsFinal"


def save_file(products, filename, relative_path="../"):
    directory = os.path.relpath(relative_path)
    file_path = os.path.join(directory, filename + ".json")

    f = open(file_path, "w")
    f.write(products.to_json())
    f.close()


def save_consolidator(products):
    save_file(products, consolidated_products_filename)


def load_file(filename, relative_path="../"):
    directory = os.path.relpath(relative_path)
    file_path = os.path.join(directory, filename + ".json")

    if os.path.isfile(file_path):
        f = open(file_path, "r")
        json_string = f.read()
        f.close()
        return json_string

    return None

def load_consolidator():
    consolidator_json = load_file(consolidated_products_filename)
    product_consolidator = ProductConsolidator()
    if consolidator_json is not None:
        product_consolidator = ProductConsolidator.from_json(consolidator_json)

    return product_consolidator


def load_reconciler():
    reconciler_json = load_file(reconciler_filename)
    reconciler = ProductModelByBrandMap()
    if reconciler_json is not None:
        reconciler = ProductModelByBrandMap.from_json(reconciler_json)

    return reconciler


def load_consolidator_and_reconciler():
    product_consolidator = load_consolidator()
    reconciler = load_reconciler()

    return product_consolidator, reconciler
