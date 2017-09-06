from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModelByBrandMap import ProductModelByBrandMap
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator, \
    save_reconciler


def create_model_name_reconcilor():
    product_consolidator = load_consolidator(relative_path="../compiled_files/")
    model_name_validator = ProductModelByBrandMap(product_consolidator)
    save_reconciler(model_name_validator, relative_path="../compiled_files/")


create_model_name_reconcilor()
