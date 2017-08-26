import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "DE", True, "Adjustable" in model))


def handle_razor_data_safety_adjustable(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "DE", True, True))


def handle_razor_data_straight(manufacturer, model, product_page, consolidator):
    # Going to have to handle the replacable ones manually
    razor_type = "Straight-Edge"
    uses_blade = False
    if "Shavette" in model:
        razor_type = "Shavette"
        uses_blade = True
    if "Strop" not in model:
        consolidator.add_razor(Razor(manufacturer, model, razor_type, uses_blade, False))


def handle_razor_data_straight_uses_blade(manufacturer, model, product_page, consolidator):
    # Going to have to handle the replacable ones manually
    if "Kit" not in model:
        consolidator.add_razor(Razor(manufacturer, model, "Shavette", True, False))


def pull_product_blocks_from_page(page):
    return page.find_all("div", {"class": "modular-prod"})


def read_product(product_block, consolidator, add_func):
    manufacturer = product_block.find("div", {"class": "manufacturer-name"}).text.strip()
    model = product_block.find("span", {"class": "prod-name"}).text
    model = model.replace(manufacturer + " ", "").strip()
    add_func(manufacturer, model, product_block, consolidator)


def check_for_next(page):
    pagination = page.find("ul", {"class": "pagination"})
    if pagination is not None:
        pages = pagination.find_all("li")
        next_button = pages[len(pages) - 1]
        link = next_button.find("a")
        if link is not None:
            return link.get("href")

    return None


def handle_product_type(url, consolidator, add_func):
    print "Loading Page: " + url
    page = load_page(url)
    product_blocks = pull_product_blocks_from_page(page)

    for product_block in product_blocks:
        read_product(product_block, consolidator, add_func)

    next_link = check_for_next(page)
    if next_link is not None:
        time.sleep(2)
        handle_product_type("https://www.westcoastshaving.com" + next_link, consolidator, add_func)


def compile_west_coast_shaving():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type(
        "https://www.westcoastshaving.com/Pre-Shave_c_14.html", product_consolidator, handle_preshave_data)

    # Soaps
    handle_product_type(
        "https://www.westcoastshaving.com/Shaving-Cream_c_15.html", product_consolidator, handle_soap_data)
    handle_product_type(
        "https://www.westcoastshaving.com/Shaving-Soaps_c_16.html", product_consolidator, handle_soap_data)
    handle_product_type(
        "https://www.westcoastshaving.com/hard-croap-shaving-cream.html", product_consolidator, handle_soap_data)

    # Brushes
    handle_product_type(
        "https://www.westcoastshaving.com/silvertip-badger-shaving-brushes.html",
        product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.westcoastshaving.com/Super-Badger-shaving-brushes.html", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.westcoastshaving.com/Best-Badger-shaving-brushes.html", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.westcoastshaving.com/Pure-Badger-shaving-brushes.html", product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.westcoastshaving.com/boar-hair-and-horse-hair-shaving-brush.html",
        product_consolidator, handle_brush_data)
    handle_product_type(
        "https://www.westcoastshaving.com/synthetic-shaving-brushes.html", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type(
        "https://www.westcoastshaving.com/closed-comb-safety-razor.html",
        product_consolidator, handle_razor_data_safety)
    handle_product_type(
        "https://www.westcoastshaving.com/butterfly-safety-razors.html", product_consolidator, handle_razor_data_safety)
    handle_product_type(
        "https://www.westcoastshaving.com/open-comb-safety-razors.html", product_consolidator, handle_razor_data_safety)
    handle_product_type(
        "https://www.westcoastshaving.com/adjustable-safety-razors.html",
        product_consolidator, handle_razor_data_safety_adjustable)
    handle_product_type(
        "https://www.westcoastshaving.com/slant-safety-razors.html", product_consolidator, handle_razor_data_safety)

    # Straight Razors
    handle_product_type(
        "https://www.westcoastshaving.com/traditional-straight-razors.html",
        product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "https://www.westcoastshaving.com/replaceable-blade-straight-razors.html",
        product_consolidator, handle_razor_data_straight_uses_blade)
    handle_product_type(
        "https://www.westcoastshaving.com/Straight-Razors_c_9.html?Attribs=105",
        product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "https://www.westcoastshaving.com/Straight-Razors_c_9.html?Attribs=137",
        product_consolidator, handle_razor_data_straight)
    handle_product_type(
        "https://www.westcoastshaving.com/Straight-Razors_c_9.html?Attribs=147&",
        product_consolidator, handle_razor_data_straight_uses_blade)

    # Blades
    handle_product_type(
        "https://www.westcoastshaving.com/5-10-pack.html", product_consolidator, handle_blade_data)
    handle_product_type(
        "https://www.westcoastshaving.com/50-and-100-blade-packs.html", product_consolidator, handle_blade_data)
    handle_product_type(
        "https://www.westcoastshaving.com/straight-razor-blades.html", product_consolidator, handle_blade_data)

    # PostShaves
    handle_product_type(
        "https://www.westcoastshaving.com/toiletries/nick-relief.html", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type(
        "https://www.westcoastshaving.com/After-Shaves_c_17.html", product_consolidator, handle_aftershave_data)
    handle_product_type(
        "https://www.westcoastshaving.com/Colognes_c_22.html", product_consolidator, handle_aftershave_data)
    
    save_consolidator(product_consolidator)

compile_west_coast_shaving()
