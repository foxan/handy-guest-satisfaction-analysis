# sample python execution code:
# scrapy runspider tripadvisor_review_scraper.py -a geo_id=g186299 -a destination_id=d192175 -o reviews.csv

import csv

with open("hotels.csv", "r") as in_file:
    reader = csv.reader(in_file, delimiter=",", quotechar='"')
    with open("get_reviews.sh", "w") as out_file:
        for row in reader:
            geo_id = row[0]
            destination_id = row[1]
            out_file.write("scrapy runspider tripadvisor_review_scraper.py -a geo_id={} -a destination_id={} -o reviews.csv\n".format(geo_id, destination_id))