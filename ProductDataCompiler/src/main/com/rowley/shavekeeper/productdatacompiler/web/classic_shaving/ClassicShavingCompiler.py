import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    if "Set" not in model:
        consolidator.add_razor(Razor(manufacturer, model, "DE", True, "Adjustable" in model))


def handle_razor_data_shavette(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "Shavette", True, False))


def handle_razor_data_straight(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "Straight-Edge", False, False))


def pull_blocks_from_page(page):
    return page.find_all("div", {"class": "product-index"})


def read_product(block, consolidator, add_func):
    container = block.find("div", {"class": "product-info"})
    brand = container.find("p").text
    model = container.find("h3").text

    model = model.replace(brand + " ", "").strip()
    add_func(brand, model, block, consolidator)


def check_for_next(page):
    pagination = page.find("div", {"id": "pagination"})
    if pagination is not None:
        links = pagination.find_all("a")
        if links is not None and len(links) > 1:
            possible_next = links[len(links) - 1]
            trigger = possible_next.find("i")
            if trigger is not None:
                return possible_next.get("href")

    return None


def handle_product_type(url, consolidator, add_func):
    time.sleep(2)
    print "Loading Page: " + url
    page = load_page(url)
    blocks = pull_blocks_from_page(page)

    for block in blocks:
        read_product(block, consolidator, add_func)

    next_link = check_for_next(page)
    if next_link is not None:
        handle_product_type("https://www.classicshaving.com" + next_link, consolidator, add_func)


def compile_classic_shaving():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type(
        "https://www.classicshaving.com/collections/pre-shave", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type(
        "https://www.classicshaving.com/collections/shaving-cream", product_consolidator, handle_soap_data)
    handle_product_type("https://www.classicshaving.com/collections/shave-soaps-and-creams-styptic",
                        product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type(
        "https://www.classicshaving.com/collections/shaving-brushes", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.classicshaving.com/collections/classic-brand-brushes", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.classicshaving.com/collections/satin-tip", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.classicshaving.com/collections/otherbrushes", product_consolidator, handle_brush_data)
    handle_product_type("https://www.classicshaving.com/collections/vie-long", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type(
        "https://www.classicshaving.com/collections/safety-razors", product_consolidator, handle_razor_data_safety)

    # Straight Razors
    handle_product_type(
        "https://www.classicshaving.com/collections/straight-razors", product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "https://www.classicshaving.com/collections/kamisori", product_consolidator, handle_razor_data_straight)
    handle_product_type("https://www.classicshaving.com/collections/replaceable-blade-straight-razors",
                        product_consolidator, handle_razor_data_shavette)

    # Blades
    handle_product_type(
        "https://www.classicshaving.com/collections/razor-blades-safes", product_consolidator, handle_blade_data)

    # PostShaves
    handle_product_type(
        "https://www.classicshaving.com/collections/nick-relief", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type(
        "https://www.classicshaving.com/collections/aftershave", product_consolidator, handle_aftershave_data)
    handle_product_type(
        "https://www.classicshaving.com/collections/aftershaves-colognes", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_classic_shaving()
