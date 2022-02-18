"""
the module creates the web app
for generating a map with the locations
of the friends for a certain Twitter account;
"""


from geopy.geocoders import Nominatim, ArcGIS
from geopy.extra.rate_limiter import RateLimiter
import folium



def get_json_dict(name):
    """
    fucntion allows the user to create json
    for a certain twitter account;
    """
    import urllib.request
    import urllib.parse
    import urllib.error
    import json
    import ssl
    import twurl

    new_dict = {}

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE



    # acct = input('Enter Twitter Account:')
    acct = name
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '10'})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)

    for user in js['users']:
        if user['location'] == '':
            continue
        location = user['location']
        name = user['screen_name']
        new_dict[name] = location

    return new_dict


def coordinates_def(adress:str):
    """
    function uses geocoders to find the coordinates
    of given location
    >>> int(coordinates_def('Stage 2, Warner Brothers\
         Burbank Studios - 4000 Warner Boulevard, Burbank, California, USA')[0])
    34
    >>> coordinates_def('')
    >>> int(coordinates_def('Bad Hersfeld, Hessen, Germany')[0])
    50
    >>> int(coordinates_def('Bad Hersfeld, Hessen, Germany')[1])
    9
    >>> coordinates_def('Bad Hersfeld, Hessen, Germany')
    (50.86952000000008, 9.712830000000054)

    """
    try:
        geolocator = ArcGIS(user_agent='_')
        geocode_function = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode_function(adress)
        if location is not None:
            return (location.latitude, location.longitude)
        else:
            geolocator = Nominatim(user_agent='_')
            location = geolocator.geocode(adress)
            if location is not None:
                return (location.latitude, location.longitude)
    except Exception:
        return None



def generate_map(json_dict:dict):
    """
    function generates the map for the points given;
    """

    the_map = folium.Map(zoom_start=1.5)
    html = """<h4>Friends locations:</h4>
    Friend's name: {},<br>
    """

    fg1 = folium.FeatureGroup(name='mark layer for location')

    for key in json_dict:
        if json_dict[key] is None:
            continue
        iframe = folium.IFrame(html=html.format(key),
        width=300,
        height=100)


        fg1.add_child(folium.Marker(location=[json_dict[key][0], json_dict[key][1]],
        popup=folium.Popup(iframe),
        icon=folium.Icon(color = "red")))



    the_map.add_child(fg1)
    the_map.add_child(folium.LayerControl())
    the_map.save('Friends_map.html')




def main(name):
    """
    the main function of the progarm
    """
    json_dict = get_json_dict(name)
    for key in json_dict:
        json_dict[key] = coordinates_def(json_dict[key])
    generate_map(json_dict)

# main()
