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

cur.execute("SELECT destination_id, name FROM hotel WHERE address IS NOT NULL AND lat IS NULL;")
rows = cur.fetchall()

with open("gmaps.key", "r") as f:
    gmaps_key = f.readline()

def get_lat_long(address):
    # sample request for Google Maps Geocoding API:
    # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
    try:
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + gmaps_key)
        lat = r.json()["results"][0]["geometry"]["location"]["lat"]
        long = r.json()["results"][0]["geometry"]["location"]["lng"]
        return lat, long
    except:
        print(address, r.json())

for row in tqdm(rows):
    try:
        destination_id = row[0]
        address = row[1]
        
        lat, long = get_lat_long(address)

        sql = """
        UPDATE hotel
        SET lat = %s, long = %s
        WHERE destination_id = %s;
        """

        cur.execute(sql, (lat, long, destination_id))
    except:
        conn.commit()

conn.commit()
conn.close()