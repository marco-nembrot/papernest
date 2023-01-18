
import json
import os
import pyproj
import pandas
import urllib.request


PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
FILE = '2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv'
COORDINATES_FILE = os.path.join(PATH, '[Coords]_{}'.format(FILE))
PROCESSED_FILE = os.path.join(PATH, 'Database.csv')
URL_SEARCH = 'https://api-adresse.data.gouv.fr/search/?q={}'
URL_REVERSE = 'https://api-adresse.data.gouv.fr/reverse/?lon={}&lat={}'
OPERATORS = {
    '20801':'Orange', 
    '20810':'SFR', 
    '20815':'Free', 
    '20820':'Bouygues'
}

def open_file(file=PROCESSED_FILE):
    return pandas.read_csv(os.path.join(PATH, file), delimiter=';', dtype='string')

# Updating rows of the drataframe --------------------------------------------------------------------------
def add_coordinates(row):
    long, lat = lamber93_to_gps(row.x, row.y)
    row.longitude = long
    row.latitude = lat

    return row

def add_postcode(row):
    address = get_address_data(row)
    row.postcode = get_postcode(address)

    return row

def set_operator(row):
    row.Operateur = OPERATORS[row.Operateur]

    return row

def update_row(row):
    return set_operator(add_postcode(row))

# Handling communcation with the external API --------------------------------------------------------------
def call_api(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data.decode('utf8'))

def get_address_data(row):
    return call_api(URL_REVERSE.format(row.longitude, row.latitude)) 

def get_query_data(q):
    return call_api(URL_SEARCH.format(urllib.parse.quote_plus(q))) 

def get_postcode(address):
    if len(address['features']) != 0:
        return address['features'][0]['properties']['postcode']
    
    return None

# More -----------------------------------------------------------------------------------------------------
def lamber93_to_gps(x, y):
    lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
    wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    x = 102980
    y = 6847973
    long, lat = pyproj.transform(lambert, wgs84, x, y)

    return long, lat