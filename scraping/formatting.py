# Files should be of the format:
# [
#    0: [name:string, sqr:double, price:double, beds:int, baths:int, distance:double, BER:double, type:string]
# ]
import pandas as pd
import csv
import re

def format_listing(listings_s, number_of_listings):
    accommodation = []
    for listing in listings_s:
        accommodation_inner = {}
        # Can use listing.title either but some listings have the same title
        try:
            accommodation_inner["name"] = listing.id
            accommodation_inner["price"] = listing.monthly_price
            # int(re.sub("[^0-9]", "", listing.monthly_price))
            try:
                if ((listing.bedrooms == 'Double Room') or (listing.bedrooms == 'Single Room') or (listing.bedrooms == 'Shared Room') or (listing.bedrooms == 'Twin Room')):
                    accommodation_inner['bedrooms'] = 1
                elif ((listing.bedrooms == 'Single & Double Room') or (listing.bedrooms == 'Double & Twin Room') or (listing.bedrooms == 'Twin & Shared Room')
                      or (listing.bedrooms == 'Double & Shared Room') or (listing.bedrooms == 'Single & Shared Room')):
                    accommodation_inner['bedrooms'] = 1
                else:
                    accommodation_inner["bedrooms"] = int(re.sub("[^0-9]", "", listing.bedrooms))
            except Exception as e:
                print(e)
                ###
            try:
                if(listing.bathrooms != None and listing.bathrooms != '' and type(listing.bathrooms) != float):
                    accommodation_inner["bathrooms"] = int(re.sub("[^0-9]", "", listing.bathrooms))
                else:
                    accommodation_inner["bathrooms"] = 0
            except:
                print(listing.bathrooms)
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
                accommodation_inner["BER"] = "NA"
            accommodation_inner["type"] = listing.sale_type
            accommodation.append(accommodation_inner)
        except Exception as e:
            print(e)
            print(listing.bedrooms)
    return accommodation


def format_to_csv(file):
    keys = file[0].keys()
    with open('scraping/houses.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(file)

def open_csv(filename):
    # accommodation = {}
    # input_file = csv.DictReader(open("scraping/houses.csv"))
    # return input_file
    return pd.read_csv(filename).to_dict('records')