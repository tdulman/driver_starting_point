import csv
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):

    lat1 = float(lat1)
    lat2 = lat2.rstrip("\n")
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3961
    return c * r * 1.4

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


with open('driver_info.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    distances = {}
    for row in readCSV:
        user_id = row[0]
        metro_id = row[1]
        driver_latitude = row[2]
        driver_longtitude = row[3]
        driver_rating = row[4]
        try:
            starting_locs = starting_locations[metro_id]
            #print("starting_locs: " + str(starting_locs))
            min_distance = 9000000000000
            for start_loc in starting_locs:
                # print(metro_id)
                # print(start_loc)
                distance = haversine(driver_latitude, driver_longtitude, start_loc[0], start_loc[1])
                if distance < min_distance:
                    min_distance = distance
            print("for driver " + str(user_id) + " minimum distance is " + str(min_distance))

        except KeyError:
            print("omg fam we don't have this Driver Users Metro ID in the starting locations file! " + metro_id)


    #     print([driver_latitude,driver_longtitude])
    #     print(metro_id)
    # print(starting_locations)




