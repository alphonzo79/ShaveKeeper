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


def pull_urls_from_page(page):
    main_container = page.find("ul", {"class": "ProductList"})
    product_blocks = main_container.find_all("li")

    urls = []
    for product_block in product_blocks:
        urls.append(product_block.find("div", {"class": "ProductDetails"}).find("a").get("href"))

    return urls


def read_product(url, consolidator, add_func):
    product_page = load_page(url)

    if product_page is not None:
        brand = product_page.find("h5", {"class": "brandName"}).text
        model = product_page.find("h1").text

        model = model.replace(brand + " ", "").strip()
        add_func(brand, model, product_page, consolidator)


def check_for_next(page):
    pagination = page.find("div", {"class": "CategoryPagination"})
    if pagination is not None:
        next_button = pagination.find("div", {"class": "Next"})
        if next_button is not None and next_button.find("a") is not None:
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
        handle_product_type(next_link, consolidator, add_func)


def compile_razor_emporium():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type("http://www.razoremporium.com/pre-shave/", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type("http://www.razoremporium.com/soaps-creams/", product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type("http://www.razoremporium.com/badger-shaving-brushes/", product_consolidator, handle_brush_data)
    handle_product_type("http://www.razoremporium.com/boar-brushes/", product_consolidator, handle_brush_data)
    handle_product_type("http://www.razoremporium.com/horse-hair-brushes/", product_consolidator, handle_brush_data)
    handle_product_type("http://www.razoremporium.com/synthetic-brushes/", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type("http://www.razoremporium.com/vintage/", product_consolidator, handle_razor_data_safety)
    handle_product_type(
        "http://www.razoremporium.com/de-safety-razors/", product_consolidator, handle_razor_data_safety)

    # Straight Razors
    handle_product_type("http://www.razoremporium.com/beginner/", product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "http://www.razoremporium.com/shavette-style/", product_consolidator, handle_razor_data_shavette)
    handle_product_type("http://www.razoremporium.com/intermediate/", product_consolidator, handle_razor_data_straight)
    handle_product_type("http://www.razoremporium.com/advanced/", product_consolidator, handle_razor_data_straight)

    # Blades
    handle_product_type("http://www.razoremporium.com/double-edge/", product_consolidator, handle_blade_data)
    handle_product_type("http://www.razoremporium.com/single-edge-se/", product_consolidator, handle_blade_data)
    handle_product_type("http://www.razoremporium.com/injector/", product_consolidator, handle_blade_data)

    # PostShaves

    # AfterShaves
    handle_product_type("http://www.razoremporium.com/after-shave/", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_razor_emporium()
