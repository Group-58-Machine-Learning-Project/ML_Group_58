# Files should be of the format:
# [
#    0: [name:string, sqr:double, price:double, beds:int, baths:int, distance:double, BER:double, type:string]
# ]
from daftlistings import Daft, Location, SearchType, PropertyType


def pull_properties(search_type):
    daft = Daft()
    daft.set_location(Location.DUBLIN)
    daft.set_search_type(search_type)
    listings = daft.search()
    return [listings, daft.total_results]



