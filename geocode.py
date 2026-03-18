from geopy.geocoders import Nominatim

def geocode_address(query: str):
    """Return (lat, lon) for an address or ZIP, or None if not found."""
    locator = Nominatim(user_agent="crime-map-prototype")
    loc = locator.geocode(query)
    if loc:
        return (loc.latitude, loc.longitude)
    return None