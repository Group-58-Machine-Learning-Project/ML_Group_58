# Files should be of the format:
# [
#    0: [name:string, sqr:double, price:double, beds:int, baths:int, distance:double, BER:double, type:string]
# ]
from daftlistings import Daft, Location, SearchType, PropertyType
import csv


def pull_properties():
    daft = Daft()
    daft.set_location(Location.DUBLIN)
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    daft.set_property_type(PropertyType.APARTMENT)
    listings = daft.search()
    return [listings, daft.total_results]


def format_listing(listings_s, number_of_listings):
    accommodation = []
    for listing in listings_s:
        accommodation_inner = {}
        # Can use listing.title either but some listings have the same title
        accommodation_inner["name"] = listing.id
        accommodation_inner["price"] = listing.price
        accommodation_inner["bedrooms"] = listing.bedrooms
        accommodation_inner["bathrooms"] = listing.bathrooms
        # Trinity lat and lon: 53.3438° N, 6.2546° W
        # co-ords of tcd: 53.3438° N, 6.2546° W
        # co-ords of ucd: 53.3065° N, 6.2255° W
        # ucd_co_ords = [53.3065, -6.2255]
        location = [53.3438, -6.2546]
        try:
            accommodation_inner["sqr"] = listing.size_meters_squared
        except Exception as e:
            accommodation_inner["sqr"] = "N/A"
        accommodation_inner["distance"] = listing.distance_to(location)
        try:
            accommodation_inner["BER"] = listing.ber
        except:
            accommodation_inner["BER"] = "N/A"
        accommodation_inner["type"] = listing.sale_type
        accommodation.append(accommodation_inner)
    return accommodation


def format_to_csv(file):
    keys = file[0].keys()
    with open('houses.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(file)
