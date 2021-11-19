
# Title:
from daftlistings import Daft, Location, SearchType, PropertyType
from scraping.scraping import pull_properties
from scraping.formatting import format_listing, format_to_csv, open_csv
import matplotlib.pyplot as plt

# Firstly, should web scrap
print("Attempting web scapping from daft.ie")

# Returns files in the format:
# 0: [name:string, sqr:double, beds:int, baths:int, distance:double, BER:double, type:string]


def main():
    # Code below searches for new daft listings which are residential rent
    listings = pull_properties(SearchType.RESIDENTIAL_RENT)
    # Comment out the line below if you want to exclude shared rent
    listings2 = pull_properties(SearchType.SHARING)
    # Combine the two searches together, and format them into a csv friendly format
    accommodation = format_listing(listings[0] + listings2[0], listings[1] + listings2[1])
    # Then inserts into a csv file so we don't have to search each time
    format_to_csv(accommodation)
    # Open csv into accommodation dictionary
    # Comment everything above, and uncomment everything below if you don't want to search each time
    # accommodation = open_csv('scraping/houses.csv')
    scatter_plots(accommodation)


def scatter_plots(accommodation):
    # four variables: bedrooms, bathrooms, BER, distance
    prices, bedrooms, bathrooms, distance = [], [], [], []
    prices_BER, BER = [], []
    for index in accommodation:
        prices.append(index['price'])
        bedrooms.append(index['bedrooms'])
        bathrooms.append(index['bathrooms'])
        distance.append(index['distance'])
        if (index['BER'] != "NA") and (type(index['BER']) != float):
            prices_BER.append(index['price'])
            BER.append(BER_convert(index['BER'], index))
    # Prices VS Bedrooms
    plt.scatter(bedrooms, prices, c='g', label="Prices VS Bedrooms")
    plt.title("Prices VS Bedrooms")
    plt.xlabel("Price")
    plt.ylabel("# Bedrooms")
    plt.show()
    # Prices VS Bathrooms
    plt.scatter(bathrooms, prices, c='g', label="Prices VS Bathrooms")
    plt.title("Prices VS Bathrooms")
    plt.xlabel("Price")
    plt.ylabel("# Bathrooms")
    plt.show()
    # Prices VS Distance
    plt.scatter(distance, prices, c='g', label="Prices VS Distance")
    plt.title("Prices VS Distance")
    plt.xlabel("Price")
    plt.ylabel("Distance")
    plt.show()
    # Prices VS BER
    plt.scatter(BER, prices_BER, c='g', label="Prices VS BER")
    plt.title("Prices VS BER")
    plt.xlabel("Price")
    plt.ylabel("BER Score, [Higher Score => Better BER]")
    plt.show()


def BER_convert(rating, index):
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
        print(rating)
        print(index)

main()

