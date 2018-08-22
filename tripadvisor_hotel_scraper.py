import psycopg2
import configparser
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# connect to the analytics database
config = configparser.ConfigParser()
config.read("connection.ini")
conn = psycopg2.connect(host=config["analytics"]["host"],
                        dbname=config["analytics"]["dbname"],
                        user=config["analytics"]["user"],
                        password=config["analytics"]["password"]
                       )

cur = conn.cursor()

cur.execute("SELECT geo_id, destination_id FROM hotel WHERE name is NULL;")
rows = cur.fetchall()

for row in tqdm(rows):
    geo_id = row[0]
    destination_id = row[1]
    
    # sample URL: https://en.tripadvisor.com.hk/Hotel_Review-d155901
    r = requests.get("https://en.tripadvisor.com.hk/Hotel_Review-d" + str(destination_id))
    soup = BeautifulSoup(r.content, "html.parser")

    try:
        name = soup.select_one("#HEADING").text
        address = soup.select_one(".address").text if not soup.select_one(".address > .detail") else soup.select_one(".address > .detail").text
        review_count = int(soup.select_one(".reviewCount").text.lower().replace("s", "").replace("review", "").replace(",", ""))
        # TODO: obtain JavaScript rendered data with brower automation tool like Selenium
        # room_count = soup.find(class_="sub_title", string="Number of rooms")
        hotel_class = None if not soup.select_one(".ui_star_rating") else int(soup.select_one(".ui_star_rating").attrs["class"][1].replace("star_", "")) / 10.0
        price_range = None if not soup.find(class_="sub_title", string="Price range") else soup.find(class_="sub_title", string="Price range").find_next().text.split("(")[0]

        sql = """
        UPDATE hotel
        SET name = %s, address = %s, review_count = %s, hotel_class = %s, price_range = %s
        WHERE destination_id = %s;
        """

        cur.execute(sql, (name, address, review_count, hotel_class, price_range, destination_id))
    except Exception as e:
        print(r.url, e)
        conn.commit()

conn.commit()
conn.close()