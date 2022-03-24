import re

from bs4 import BeautifulSoup


ITEM_HTML = '''<html><head></head><body>
<li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
    <article class="product_pod">
            <div class="image_container">
                    <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>
            </div>
                <p class="star-rating Three">
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                </p>
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
            <div class="product_price">
        <p class="price_color">£51.77</p>
<p class="instock availability">
    <i class="icon-ok"></i>
        In stock
</p>
    <form>
        <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
    </form>
            </div>
    </article>
</li>
</body></html>
'''


class ParsedItemLocators:
    """
    Locators for an item in the HTML page.
    This allows us to easily see what our code will be looking at
    as well as change it quickly if we notice it is now different.
    """
    NAME_LOCATOR = 'article.product_pod h3 a'
    LINK_LOCATOR = 'article.product_pod h3 a'
    PRICE_LOCATOR = 'article.product_pod p.price_color'
    RATING_LOCATOR = 'article.product_pod p.star-rating'


class ItemParser:

    """
    A example class to take in an HTML page or content, and find properties of an item
    in it.
    """
    def __init__(self, page) -> None:
        self.soup = BeautifulSoup(page, 'html.parser')

    def name(self):
        locator = ParsedItemLocators.NAME_LOCATOR #CSS locator
        item_name = self.soup.select_one(locator).attrs.get('title', [])
        # item_name = soup.select_one(locator).attrs['title']
        return item_name

    def link(self):
        locator = ParsedItemLocators.LINK_LOCATOR
        item_url = self.soup.select_one(locator).attrs.get('href', [])
        return item_url

    def price(self):
        locator = ParsedItemLocators.PRICE_LOCATOR
        item_price = self.soup.select_one(locator).string
        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))

    def rating(self):
        locator = ParsedItemLocators.RATING_LOCATOR
        star_rating_element = self.soup.select_one(locator)
        classes = star_rating_element.attrs['class']
        rating = filter(lambda x: x != 'star-rating', classes)
        return next(rating)


item = ItemParser(ITEM_HTML)
print(item.name())
print(item.price())
print(item.rating())