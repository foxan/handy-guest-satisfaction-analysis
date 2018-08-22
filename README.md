## handy Guest Satisfaction Analysis

![handy heatmap](/img/handy_heatmap.png)

### Problem

As handy devices are launched and deployed to more hotels around the world, we are interested to see if it has a positive impact to guest experience overall. In this project, we will use TripAdvisor reviews as a proxy to measure handy's impact on hotel guest experience.

### Repository

This repository contains both Python scripts to extract data from TripAdvisor (hotels, reviews) and Google Maps (cities, lat, long), and data analysis (exploratory data analysis, prediction model) in Jupyter notebooks.

Explanations of what each file does:

1. Exploratory Data Analysis.ipynb

> This Jupyter notebook contains exploratory data analysis on the given dataset (hotels.csv) so that we can have a better understanding on the problem we are trying to solve and what kind of data is needed.

2. tripadvisor_hotel_scraper.py

> This script is used to scrap metadata of hotels from TripAdvisor, such as `name`, `address`, `review_count`, `hotel_class` and `price_range`, which can be useful features in predicting ratings of hotels.

3. hotel_location_geocoder.py

> This script is used to obtain `latitude` and `longitude` of hotels from [Google Maps Geocoding API](https://developers.google.com/maps/documentation/javascript/geocoding) so that we can use it to create visualizations such as heatmaps.

4. city_name_geocoder.py

> This script is used to get `city` / `country` name for hotel locations from Google Maps Geocoding API so that we can provide more context and do analysis on `city` level.

5. tripadvisor_review_scraper.py, get_reviews.py, get_reviews.sh

> `Scrapy` library is used to do web crawling on TripAdvisor.
>
> `tripadvisor_review_scraper.py` contains the actual spider to crawl and parse reviews on TripAdvisor, which accepts `geo_id` and `destination_id` as input. 
>
> `get_reviews.py` generates scripts to run the spiders (e.g. scrapy runspider tripadvisor_review_scraper.py -a geo_id=g1019668 -a destination_id=d7046880 -o reviews.csv).
>
> `get_reviews.sh` contains the actual bash script which is executed on an AWS EC2 instance to do the crawling.

6.  TripAdvisor Rating Prediction.ipynb

> This Jupyter notebook contains t-test to see whether ratings after handy launch are statistically greater than ratings before handy launch, and prediction model (linear regression) to predict hotel TripAdvisor ratings after launching handy for a year.

### Installation

`pip install -r requirements.txt`
