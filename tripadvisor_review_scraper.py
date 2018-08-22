from requests_html import HTMLSession
import scrapy
import re
import math

def url_generator(geo_id, destination_id):
    MAIN_URL = "https://en.tripadvisor.com.hk/Hotel_Review-" + geo_id + "-" + destination_id
    URL_TEMPLATE = MAIN_URL + "-Reviews-or%s"

    # get number of reviews in order to decide number of pages for scraping
    session = HTMLSession()
    r = session.get(MAIN_URL)
    review_count_element = r.html.find(".reviewCount", first=True)
    review_count = int(review_count_element.text.replace(" reviews", "").replace(",", ""))
    NUM_PAGES = math.ceil(review_count / 5) # every page has 5 reviews

    # save review count for cross check of scraping results
    with open("hotel_review_count.csv", "a") as f:
        f.write("{},{},{}\n".format(geo_id, destination_id, review_count))

    for page in range(NUM_PAGES):
        yield URL_TEMPLATE % (page * 5)

class TripAdvisorReviewSpider(scrapy.Spider):
    name = "tripadvisor"

    def __init__(self, geo_id=None, destination_id=None, *args, **kwargs):
        super(TripAdvisorReviewSpider, self).__init__(*args, **kwargs)
        self.start_urls = list(url_generator(geo_id, destination_id))
        self.geo_id = geo_id
        self.destination_id = destination_id

    def parse(self, response):
        for review in response.css(".reviewSelector"):
            id = review.css("::attr(id)").extract_first()
            if id.startswith("review_title"):
                continue
            print(review.css(".quote ::text"))

            # TODO: save output to database instead of csv
            yield {
                "geo_id": self.geo_id,
                "destination_id": self.destination_id,
                "review_id": id.replace("review_", ""),
                "date": review.css(".ratingDate").xpath("@title").extract_first(),
                "title": review.css(".quote ::text").extract_first(),
                "body": review.css(".partial_entry ::text").extract_first(),
                "rating": int(review.css(".ui_bubble_rating ::attr(class)").re(r"ui_bubble_rating bubble_(\d\d)")[0])/10.0,
            }