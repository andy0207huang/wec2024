from geopy.geocoders import Nominatim


def convertToCountry(Lat: float,Lon: float) -> str:
    geolocator = Nominatim(user_agent="WEC2024")

    location = geolocator.reverse(f"{Lat},{Lon}", language="en")

    return location.raw["address"]["country"]

if __name__ == "__main__":
    country = convertToCountry(44.232723, 20.979138)
    print(country)  