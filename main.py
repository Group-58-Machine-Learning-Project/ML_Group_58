
# Title:

from scraping import pull_properties, format_listing, format_to_csv

# Firstly, should web scrap
print("Attempting web scapping from daft.ie")

# Returns files in the format:
# 0: [name:string, sqr:double, beds:int, baths:int, distance:double, BER:double, type:string]


def main():

    # Code below searches for new daft listings
    listings = pull_properties()
    # Then formats to a csv desirable style [{}]
    accommodation = format_listing(listings[0], listings[1])
    # Then inserts into a csv file so we don't have to search each time
    format_to_csv(accommodation)


main()

