import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    if "Set" not in model:
        consolidator.add_razor(Razor(manufacturer, model, "DE", True, "Adjustable" in model))


def handle_razor_data_shavette(manufacturer, model, product_page, consolidator):
    # Going to have to handle the replacable ones manually
    razor_type = "Shavette"
    uses_blade = True
    consolidator.add_razor(Razor(manufacturer, model, razor_type, uses_blade, False))


def handle_razor_data_straight(manufacturer, model, product_page, consolidator):
    # Going to have to handle the replacable ones manually
    razor_type = "Straight-Edge"
    uses_blade = False
    consolidator.add_razor(Razor(manufacturer, model, razor_type, uses_blade, False))


def pull_urls_from_page(page):
    main_container = page.find("div", {"class": "collection-main"})
    product_blocks = main_container.find_all("li")

    urls = []
    for product_block in product_blocks:
        urls.append(product_block.find("a", {"class": "prod-th"}).get("href"))

    return urls


def read_product(url, consolidator, add_func):
    product_page = load_page("https://shavenation.com" + url)

    meta_data = product_page.find("meta", {"name": "twitter:data2"})
    brand = meta_data.get("content")

    if brand is None or len(brand) is 0:
        brand = product_page.find("h2", {"itemprop": "brand"}).text

    model = product_page.find("h1", {"class": "page-title"}).text

    model = model.replace(brand + " ", "").strip()
    add_func(brand, model, product_page, consolidator)


def check_for_next(page):
    pagination = page.find("div", {"class": "paginate"})
    if pagination is not None:
        next_button = pagination.find("span", {"class": "next"})
        if next_button is not None:
            return next_button.find("a").get("href")

    return None


def handle_product_type(url, consolidator, add_func):
    print "Loading Page: " + url
    page = load_page(url)
    urls = pull_urls_from_page(page)

    for url in urls:
        time.sleep(2)
        read_product(url, consolidator, add_func)

    next_link = check_for_next(page)
    if next_link is not None:
        handle_product_type("https://www.shavenation.com" + next_link, consolidator, add_func)


def compile_shave_nation():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type("https://shavenation.com/collections/pre-shave", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type(
        "https://shavenation.com/collections/all-shaving-creams", product_consolidator, handle_soap_data)
    handle_product_type(
        "https://shavenation.com/collections/all-shaving-soaps", product_consolidator, handle_soap_data)
    handle_product_type(
        "https://shavenation.com/collections/shaving-sticks", product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type(
        "https://shavenation.com/collections/brushes", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type(
        "https://shavenation.com/collections/safety-razors", product_consolidator, handle_razor_data_safety)

    # Straight Razors
    handle_product_type(
        "https://shavenation.com/collections/shavette-razors", product_consolidator, handle_razor_data_shavette)
    handle_product_type(
        "https://shavenation.com/collections/straight-razors", product_consolidator, handle_razor_data_straight)

    # Blades
    handle_product_type("https://shavenation.com/collections/de-razor-blades", product_consolidator, handle_blade_data)
    handle_product_type(
        "https://shavenation.com/collections/single-edge-blades", product_consolidator, handle_blade_data)

    # PostShaves
    handle_product_type(
        "https://shavenation.com/collections/all-shaving-remedies", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type(
        "https://shavenation.com/collections/aftershave", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_shave_nation()
