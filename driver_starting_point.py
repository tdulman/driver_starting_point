import csv
from math import radians, cos, sin, asin, sqrt


with open('driver_info.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        user_id = row[0]
        metro_id = row[1]
        driver_latitude = row[2]
        driver_longtitude = row[3]
        driver_rating = row[4]


with open('all_driver_starting_points.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    starting_locations = {}

    for row in readCSV:
        metro_name = row[0]
        SP_metro_id = row[1]
        starting_point_id = row[2]
        starting_point_latitude = row[3]
        starting_point_longtitude = row[4]
        percentage = row[-1]

        try:
            starting_locations[SP_metro_id]
            starting_locations[SP_metro_id].append([starting_point_latitude, starting_point_longtitude])
        except KeyError:
            starting_locations[SP_metro_id] = [[starting_point_latitude, starting_point_longtitude]]

    print(starting_locations)

# def haversine(lon1, lat1, lon2, lat2):
#
#     lon1 = float(driver_longtitude)
#     lon2 = lon2.rstrip("\n")
#     lon2 = float(starting_point_longtitude)
#     lat1 = float(driver_latitude)
#     lat2 = float(starting_point_longtitude)
#
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 3961
#     return c * r * 1.4



