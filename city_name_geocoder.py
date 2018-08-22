import requests
import psycopg2
import configparser
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

cur.execute("SELECT geo_id, lat, long FROM city WHERE name IS NULL;")
rows = cur.fetchall()

with open("gmaps.key", "r") as f:
    gmaps_key = f.readline()

def get_name(lat, long):
    # sample request for Google Maps Geocoding API:
    # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
    try:
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + str(lat) + "," + str(long) + "&key=" + gmaps_key)
        address_components = r.json()["results"][0]["address_components"]
        for a in address_components:
            # lookup for city name first, if not exist then lookup for country name
            if a["types"] == ['locality', 'political']:
                name = a["long_name"]
            elif a["types"] == ['country', 'political']:
                name = a["long_name"]
        return name
    except:
        print(lat, long, r.json())


for row in tqdm(rows):
    try:
        geo_id = row[0]
        lat = row[1]
        long = row[2]
        
        name= get_name(lat, long)

        sql = """
        UPDATE city
        SET name = %s
        WHERE geo_id = %s;
        """

        cur.execute(sql, (name, geo_id))
    except:
        conn.commit()

conn.commit()
conn.close()