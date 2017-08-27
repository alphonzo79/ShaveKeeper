import time

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import Razor, Blade, Brush
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.web.WebFuncsCommon import load_page, handle_aftershave_data, \
    handle_postshave_data, handle_blade_data, handle_preshave_data, handle_soap_data, handle_brush_data


def handle_paa_soap_data(manufacturer, model, product_page, consolidator):
    if "Aftershave" in model:
        handle_aftershave_data(manufacturer, model, product_page, consolidator)
    else:
        handle_soap_data(manufacturer, model, product_page, consolidator)


def handle_razor_data_safety(manufacturer, model, product_page, consolidator):
    consolidator.add_razor(Razor(manufacturer, model, "DE", True, "Adjustable" in model))


def pull_product_blocks_from_page(page):
    return page.find_all("div", {"class": "col-product"})


def read_product(product_block, brand, consolidator, add_func):
    model = product_block.find("p", {"class": "grid-link__title"}).text
    model = model.replace(brand + " ", "").strip()
    add_func(brand, model, product_block, consolidator)


def check_for_next(page):
    pagination = page.find("ul", {"class": "pagination-custom"})
    if pagination is not None:
        pages = pagination.find_all("li")
        next_button = pages[len(pages) - 1]
        if next_button.get("class") is None or "disabled" not in next_button.get("class")[0]:
            return next_button.find("a").get("href")

    return None


def handle_product_type(url, brand, consolidator, add_func):
    time.sleep(2)
    print "Loading Page: " + url
    page = load_page(url)
    product_blocks = pull_product_blocks_from_page(page)

    for product_block in product_blocks:
        read_product(product_block, brand, consolidator, add_func)

    next_link = check_for_next(page)
    if next_link is not None:
        handle_product_type("http://www.phoenixartisanaccoutrements.com" + next_link, brand, consolidator, add_func)


def compile_phoenix_artisan_accoutrements():
    product_consolidator = load_consolidator()

    # Preshaves
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/pre-shave-1",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_preshave_data)
    #todo handle that one manually

    # Soaps
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/phoenix-shaving-soap",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/crown-king-shaving-soap-1",
                        "Crown King", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/antiga-barbearia-de-bairro",
                        "Antiga Barbearia de Bairro", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/arko",
                        "Arko", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/beaver-woodwright",
                        "Black Ship Grooming", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/cella",
                        "Cella", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/haslinger",
                        "Haslinger", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/the-holy-black-shaving-soap",
                        "The Holy Black", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/k-shave-worx-shaving-soap",
                        "K Shave Worx", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/la-toja-shaving-soap",
                        "La Toja", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/local-gent-shaving-co-llc",
                        "Local Gent Shaving Co.", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/mitchells-wool-fat",
                        "Mitchell's Wool Fat", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/morsel-shaving-soap",
                        "Myrsol", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/castel-bel-porto-portus-cale",
                        "Portus Cale", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/proraso-shave-soap",
                        "Proraso", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/razo-rock-shaving-soap-1",
                        "RazoRock", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/soap-commander-shave-soap",
                        "Soap Commander", product_consolidator, handle_paa_soap_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/tabac-original",
                        "Tabac", product_consolidator, handle_paa_soap_data)

    # Brushes
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/phoenix-shaving-brushes",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_brush_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/crown-king-shaving-brushes",
                        "Crown King", product_consolidator, handle_brush_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/omega",
                        "Omega", product_consolidator, handle_brush_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/semogue",
                        "Semogue", product_consolidator, handle_brush_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/vie-long-shaving-brushes",
                        "Vie Long", product_consolidator, handle_brush_data)

    # Safety Razors
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/phoenix-artisan-accoutrements-razors",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_razor_data_safety)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/edwin-jagger-razors",
                        "Edwin Jagger", product_consolidator, handle_razor_data_safety)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/fat-tip",
                        "Fat Tip", product_consolidator, handle_razor_data_safety)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/merkur",
                        "Merkur", product_consolidator, handle_razor_data_safety)

    # Straight Razors

    # Blades

    # PostShaves

    # AfterShaves
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/phoenix-aftershave-colognes",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/crown-king-aftershave-cologne-1",
                        "Crown King", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/aftershave-lotion",
                        "Phoenix Artisan Accoutrements", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/4711",
                        "4711", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/aqua-velva",
                        "Aqua Velva", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/black-ship-grooming",
                        "Black Ship Grooming", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/cella",
                        "Cella", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/floid",
                        "Floid", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/the-holy-black-aftershave",
                        "The Holy Black", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/irisch-moos",
                        "Irisch Moos", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/k-shave-worx-aftershave",
                        "K Shave Worx", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/la-toja-aftershave-lotion",
                        "La Toja", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/local-gent-aftershave",
                        "Local Gent Shaving Co.", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/myrsol",
                        "Myrsol", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/proraso-aftershave",
                        "Proraso", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/shaving-soap",
                        "RazoRock", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/tabac-aftershave",
                        "Tabac", product_consolidator, handle_aftershave_data)
    handle_product_type("http://phoenixartisanaccoutrements.com/collections/the-stray-whisker",
                        "The Stray Whisker", product_consolidator, handle_aftershave_data)

    save_consolidator(product_consolidator)


compile_phoenix_artisan_accoutrements()
