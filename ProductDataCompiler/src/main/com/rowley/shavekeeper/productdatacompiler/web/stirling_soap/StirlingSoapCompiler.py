import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model + " - Standard", "DE", True, False))
    consolidator.add_razor(Razor(manufacturer, model + " - Aggressive", "DE", True, False))
    consolidator.add_razor(Razor(manufacturer, model + " - Open Comb", "DE", True, False))


def pull_product_blocks_from_page(page):
    return page.find_all("span", {"class": "ProductName"})


def read_product(product_block, consolidator, add_func):
    brand = "Stirling Soap Co."
    model = product_block.text
    model = model.replace(brand + " ", "").strip()
    add_func(brand, model, product_block, consolidator)


def handle_product_type(url, consolidator, add_func):
    time.sleep(2)
    print "Loading Page: " + url
    page = load_page(url)
    product_blocks = pull_product_blocks_from_page(page)

    for product_block in product_blocks:
        read_product(product_block, consolidator, add_func)


def compile_stirling_soap():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type("https://www.stirlingsoap.com/beard-pre-shave/", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type("https://www.stirlingsoap.com/shave-soap/", product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type("https://www.stirlingsoap.com/shave-brushes/", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type("https://www.stirlingsoap.com/razors/", product_consolidator, handle_razor_data_safety)

    # Straight Razors

    # Blades

    # PostShaves
    handle_product_type("https://www.stirlingsoap.com/witch-hazel-aloe/", product_consolidator, handle_postshave_data)
    handle_product_type("https://www.stirlingsoap.com/post-shave-balm/", product_consolidator, handle_postshave_data)
    handle_product_type("https://www.stirlingsoap.com/shea-butter/", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type("https://www.stirlingsoap.com/aftershave-splash/", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_stirling_soap()
