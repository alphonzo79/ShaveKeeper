import urllib2

import time
from bs4 import BeautifulSoup

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PreShave, AfterShave, PostShave, \
    Soap, Blade, Razor, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator_and_reconciler, \
    load_consolidator, save_consolidator


def handle_preshave_data(manufacturer, model, product_page, consolidator):
    consolidator.add_pre_shave(PreShave(manufacturer, model))


def handle_soap_data(manufacturer, model, product_page, consolidator):
    consolidator.add_soap(Soap(manufacturer, model))


def handle_brush_data(manufacturer, model, product_page, consolidator):
    consolidator.add_brush(Brush(manufacturer, model))


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "DE", True, "Adjustable" in model))


def handle_razor_data_straight(manufacturer, model, product_page, consolidator):
    # Going to have to handle the replacable ones manually
    razor_type = "Straight-Edge"
    uses_blade = False
    consolidator.add_razor(Razor(manufacturer, model, razor_type, uses_blade, False))


def handle_feather_artist_club(manufacturer, model, product_page, consolidator):
    if "Blades" in model:
        consolidator.add_blade(Blade(manufacturer, model))
    else:
        consolidator.add_razor(Razor(manufacturer, model, "Straight-Edge", True, False))


def handle_blade_data(manufacturer, model, product_page, consolidator):
    consolidator.add_blade(Blade(manufacturer, model))


def handle_postshave_data(manufacturer, model, product_page, consolidator):
    consolidator.add_post_shave(PostShave(manufacturer, model))


def handle_aftershave_data(manufacturer, model, product_page, consolidator):
    if "Witch Hazel" in model:
        consolidator.add_post_shave(PostShave(manufacturer, model))
    elif "Combo Pack" not in model:
        consolidator.add_after_shave(AfterShave(manufacturer, model))


def load_page(url):
    headers = {'User-Agent': 'Mozilla 5.10'}
    try:
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        return BeautifulSoup(response.read(), 'html.parser')
    except urllib2.HTTPError as e:
        print e.code + " ::: " + url
        return None


def pull_urls_from_page(page):
    results = []
    links = page.find_all("a", text="View")
    for link in links:
        results.append(link.get("href"))
    return results


def read_product(url, consolidator, add_func):
    product_page = load_page("https://www.italianbarber.com" + url)
    if product_page is not None:
        manufacturer = product_page.find("div", {"id": "tbs1"}).text.strip()
        model = product_page.find("div", {"class": "product-header"}).text
        model = model.replace(manufacturer + " ", "").strip()
        add_func(manufacturer, model, product_page, consolidator)


def check_for_next(page):
    pagination = page.find("ul", {"class": "pagination"})
    if pagination is not None:
        pages = pagination.find_all("li")
        next_button = pages[len(pages) - 1]
        if next_button.get("class") is not "disabled":
            return next_button.find("a").get("href")

    return None


def handle_product_type(url, consolidator, add_func):
    print "Loading Page: " + url
    page = load_page(url)
    links = pull_urls_from_page(page)

    for link in links:
        read_product(link, consolidator, add_func)
        time.sleep(2)

    next_link = check_for_next(page)
    if next_link is not None:
        handle_product_type("https://www.italianbarber.com" + next_link, consolidator, add_func)


def compile_italian_barber():
    product_consolidator = load_consolidator()

    # Preshaves
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/pre-shave", product_consolidator, handle_preshave_data)
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/shave-oil", product_consolidator, handle_preshave_data)

    # Soaps
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/brushless-creams-gels", product_consolidator, handle_soap_data)
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/creams-soaps", product_consolidator, handle_soap_data)

    # Brushes
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/brushes/brushes", product_consolidator, handle_brush_data)
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/brushes/brushes-vegan-synthetic",
    #     product_consolidator, handle_brush_data)
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/brushes-vegan-synthetic", product_consolidator, handle_brush_data)

    # Safety Razors
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/safety-razors/safety-razors",
    #     product_consolidator, handle_razor_data_safety)

    # Straight Razors
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/straight-razors", product_consolidator, handle_razor_data_straight)

    # Feather Artist Club
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/feather-artist-club-blades",
    #     product_consolidator, handle_feather_artist_club)

    # Blades
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/razor-blades", product_consolidator, handle_blade_data)

    # PostShaves
    # handle_product_type(
    #     "https://www.italianbarber.com/collections/alum", product_consolidator, handle_postshave_data)

    # AfterShaves
    handle_product_type(
        "https://www.italianbarber.com/collections/aftershaves-balms-1/aftershaves-balms",
        product_consolidator, handle_aftershave_data)
    handle_product_type(
        "https://www.italianbarber.com/collections/aftershaves-balms-1/fragrances",
        product_consolidator, handle_aftershave_data)
    handle_product_type(
        "https://www.italianbarber.com/collections/aftershaves-balms-1/skincare",
        product_consolidator, handle_postshave_data)
    handle_product_type(
        "https://www.italianbarber.com/collections/aftershaves-balms-1/toner-cleanser",
        product_consolidator, handle_postshave_data)
    handle_product_type(
        "https://www.italianbarber.com/collections/fragrances-1/aftershaves-balms",
        product_consolidator, handle_aftershave_data)
    handle_product_type(
        "https://www.italianbarber.com/collections/fragrances-1/fragrances",
        product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)

compile_italian_barber()
