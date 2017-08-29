import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def pull_product_blocks_from_page(page):
    return page.find_all("div", {"class": "simpleCart_shelfItem"})


def read_product(product_block, consolidator, add_func):
    meta_data = product_block.find("ul", {"class": "text book padding"})
    # Filter out Sample packs and headers
    if meta_data is None:
        return

    brand = ""
    model = ""

    title_text = product_block.find("h3", {"class": "item_name"}).text
    if " - " in title_text:
        split = title_text.split(" - ")
        brand = split[0]
        model = split[1]
    else:
        brand = meta_data.find("li").text.split("Manufacturer:")[1].strip()
        model = title_text

    model = model.replace(brand + " ", "").strip()
    add_func(brand, model, product_block, consolidator)


def handle_product_type(url, consolidator, add_func):
    time.sleep(2)
    print "Loading Page: " + url
    page = load_page(url)
    product_blocks = pull_product_blocks_from_page(page)

    for product_block in product_blocks:
        read_product(product_block, consolidator, add_func)


def compile_try_a_blade():
    product_consolidator = load_consolidator()

    # Preshaves
    # Soaps
    # Brushes
    # Safety Razors
    # Straight Razors

    # Blades
    handle_product_type("http://tryablade.com/artistclub", product_consolidator, handle_blade_data)
    handle_product_type("http://tryablade.com/blade", product_consolidator, handle_blade_data)
    handle_product_type("http://tryablade.com/newoldstock", product_consolidator, handle_blade_data)
    handle_product_type("http://tryablade.com/shavette", product_consolidator, handle_blade_data)
    handle_product_type("http://tryablade.com/singleedge", product_consolidator, handle_blade_data)

    # PostShaves
    # AfterShaves

    save_consolidator(product_consolidator)


compile_try_a_blade()
