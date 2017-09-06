import os

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModelByBrandMap import ProductModelByBrandMap

consolidated_products_filename = "ConsolidatedProducts"
reconciler_filename = "Reconciler"
flat_list_filename = "ProductsFinal"


def save_file(products, filename, relative_path="../../compiled_files/"):
    directory = os.path.relpath(relative_path)
    file_path = os.path.join(directory, filename + ".json")

    f = open(file_path, 'w')
    f.write(products.to_json())
    f.close()


def save_consolidator(products, relative_path="../../compiled_files/"):
    save_file(products, consolidated_products_filename, relative_path)


def save_reconciler(reconciler, relative_path="../../compiled_files/"):
    save_file(reconciler, reconciler_filename, relative_path)


def load_file(filename, relative_path="../../compiled_files/"):
    directory = os.path.relpath(relative_path)
    file_path = os.path.join(directory, filename + ".json")

    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        json_string = f.read()
        f.close()
        return json_string

    return None

def load_consolidator(relative_path="../../compiled_files/"):
    consolidator_json = load_file(consolidated_products_filename, relative_path)
    product_consolidator = ProductConsolidator()
    if consolidator_json is not None:
        product_consolidator = ProductConsolidator.from_json(consolidator_json)

    return product_consolidator


def load_reconciler(relative_path="../../compiled_files/"):
    reconciler_json = load_file(reconciler_filename, relative_path)
    reconciler = ProductModelByBrandMap()
    if reconciler_json is not None:
        reconciler = ProductModelByBrandMap.from_json(reconciler_json)

    return reconciler


def load_consolidator_and_reconciler(relative_path="../../compiled_files/"):
    product_consolidator = load_consolidator(relative_path)
    reconciler = load_reconciler(relative_path)

    return product_consolidator, reconciler
