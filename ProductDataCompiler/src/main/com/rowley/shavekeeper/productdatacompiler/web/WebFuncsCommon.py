import urllib2

from bs4 import BeautifulSoup

from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModels import PreShave, Soap, Blade, PostShave, \
    AfterShave, Brush


def handle_preshave_data(manufacturer, model, product_page, consolidator):
    consolidator.add_pre_shave(PreShave(manufacturer, model))


def handle_soap_data(manufacturer, model, product_page, consolidator):
    if "Aftershave" not in model and "Sample" not in model:
        consolidator.add_soap(Soap(manufacturer, model))


def handle_brush_data(manufacturer, model, product_page, consolidator):
    consolidator.add_brush(Brush(manufacturer, model))


def handle_blade_data(manufacturer, model, product_page, consolidator):
    if "Sampler" not in model:
        consolidator.add_blade(Blade(manufacturer, model))


def handle_postshave_data(manufacturer, model, product_page, consolidator):
    consolidator.add_post_shave(PostShave(manufacturer, model))


def handle_aftershave_data(manufacturer, model, product_page, consolidator):
    if "Witch Hazel" in model:
        consolidator.add_post_shave(PostShave(manufacturer, model))
    elif "Combo Pack" not in model and "Pre Shave" not in model\
            and "Shaving Cream" not in model and "Sample" not in model:
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
