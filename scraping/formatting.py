# Files should be of the format:
# [
#    0: [name:string, sqr:double, price:double, beds:int, baths:int, distance:double, BER:double, type:string]
# ]
import pandas as pd
import csv
import re
import numpy as np
import pandas as pd

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
                accommodation_inner["BER"] = BER_convert(listing.ber)
            except:
                accommodation_inner["BER"] = 0
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

def BER_convert(rating):
    # SI_666 = BER Exempt
    score = 0
    if rating == 'SI_666':
        return score
    elif rating == 'F':
        return 2
    elif rating == 'G':
        return 1
    try:
        rate = list(rating)
        temp = int(rate[1])
        score = temp
        if rate[0] == 'A':
            return score + 10
        elif rate[0] == 'B':
            return score + 7
        elif rate[0] == 'C':
            return score + 4
        elif rate[0] == 'D':
            return score + 3
        elif rate[0] == 'E':
            return score + 1
        else:
            print("Error: BER rating missing")
    except:
        if rating != 'NA':
            print(rating)

def format_listings_for_models():
    # [prices, bedrooms, bathrooms, distance, BER]
    # df = pd.read_csv("houses_copy.csv")
    df = pd.read_csv("C:/Users/John/Code/ML/ML_Group/scraping/houses.csv")
    x_bedrooms = df.iloc[:, 2]  # Contains the first column of X values
    x_bathrooms = df.iloc[:, 3]  # Contains the second colunm of X values
    x_distance = df.iloc[:, 5]  # Contains the first column of X values
    x_ber = df.iloc[:, 6]  # Contains the second colunm of X values
    X = np.column_stack((x_bedrooms, x_bathrooms, x_distance, x_ber))  # Contains the combination of the two X columns
    y_2 = df.iloc[:, 1]  # Contains the y value column
    y = []
    X = []
    inc = 0
    for i in x_bedrooms:
        # X.append([int(x_bedrooms[inc]), int(x_bathrooms[inc]), round(x_distance[inc], 3), int(x_ber[inc])])
        if(0 <= x_ber[inc] and x_ber[inc] <= 14):
            X.append([int(x_bedrooms[inc]), int(x_bathrooms[inc]), int(x_ber[inc])])
            y.append(y_2[inc])
        inc = inc + 1
    return [y, X]