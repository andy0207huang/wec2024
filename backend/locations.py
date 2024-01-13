from geopy.geocoders import Nominatim


def convertToCountry(Lat: float,Lon: float) -> str:
    
    # Init Nominatim object
    geolocator = Nominatim(user_agent="WEC2024")
        
    try:
        # Gets the geolocation data
        location = geolocator.reverse(f"{Lat},{Lon}", language="en")

        # Gets the country
        country = location.raw["address"]["country"]
    
    except Exception as e:
        # If it can't find the country, set as Na
        country = "Na"

    return country

if __name__ == "__main__":
    country = convertToCountry(44.232723, 20.979138)
    print(country)  