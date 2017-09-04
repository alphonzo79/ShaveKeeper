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
    containers = page.find_all("div", {"class": "product-container"})
    urls = []
    for container in containers:
        urls.append(container.find("a", {"class": "product-image"}).get("href"))

    return urls


def read_product(url, consolidator, add_func):
    product_page = load_page(url)

    brand = ""
    table_rows = product_page.find_all("tr")
    for row in table_rows:
        if "Manufacturer" in row.find("th").text:
            brand = row.find("td").text
            break

    model = product_page.find("h1", {"itemprop": "name"}).text

    model = model.replace(brand + " ", "").strip()
    # print brand + " : " + model
    add_func(brand, model, product_page, consolidator)


def check_for_next(page):
    pagination = page.find("div", {"class": "pages"})
    if pagination is not None:
        links = pagination.find_all("a")
        if links is not None and len(links) > 1:
            possible_next = links[len(links) - 1]
            trigger = possible_next.find("i")
            if trigger is not None:
                return possible_next.get("href")

    return None


def handle_product_type(url, consolidator, add_func):
    print "Loading Page: " + url
    page = load_page(url)
    urls = pull_urls_from_page(page)

    for product_url in urls:
        time.sleep(2)
        read_product(product_url, consolidator, add_func)

    next_link = check_for_next(page)
    if next_link is not None:
        handle_product_type(next_link, consolidator, add_func)


def compile_royal_shave():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type(
        "https://www.royalshave.com/shaving-products/pre-shave", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type(
        "https://www.royalshave.com/shaving-products/shaving-cream", product_consolidator, handle_soap_data)
    handle_product_type(
        "https://www.royalshave.com/shaving-products/shaving-soap", product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type("https://www.royalshave.com/shaving-brushes", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type(
        "https://www.royalshave.com/razors/safety-razor/safety-razors", product_consolidator, handle_razor_data_safety)

    # Straight Razors
    handle_product_type("https://www.royalshave.com/razors/straight-razors/straight-razors",
                        product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "https://www.royalshave.com/razors/straight-razors/shavettes", product_consolidator, handle_razor_data_shavette)

    # Blades
    handle_product_type(
        "https://www.royalshave.com/razors/safety-razor/blades", product_consolidator, handle_blade_data)

    # PostShaves
    handle_product_type(
        "https://www.royalshave.com/shaving-products/irritation", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type(
        "https://www.royalshave.com/shaving-products/aftershave", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_royal_shave()
