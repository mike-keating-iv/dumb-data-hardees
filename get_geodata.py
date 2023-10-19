###get_geodata.py 
###
# Import modules
import pandas as pd, geopy, geopandas
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance
import matplotlib.pyplot as plt

cjs = pd.read_csv('cjs.csv', dtype = str)
hardees = pd.read_csv('hardees.csv', dtype = str)

#Concatanate scraped address data of HD and CJ restaurants
geodata = pd.concat([hardees,cjs], ignore_index = True)
full_address = []
for n in range(len(geodata)):
    street = str(geodata['street_address'][n])
    city = str(geodata['city'][n])
    state = str(geodata['state'][n])
    postal = str(geodata['postal_code'][n])
    full_address.append(f'{street}, {city}, {state} {postal}')
    
geodata['full_address'] = full_address

##Obtain Longitude and Latitute using geopy and OpenCage
geolocator = OpenCage(api_key = '6e44c385bc9e4652bde2f3817b7e6dff', user_agent='mike-keating-iv', timeout = None)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 0.067) #apply rate limiter to avoid time out errors
print('Getting coord....')
geodata['coordinates'] = geodata['full_address'].apply(geocode).apply(lambda loc: tuple((loc.latitude, loc.longitude)) if loc else None)

#loop in small chunks
geodata.to_csv('geodata', index = False)
