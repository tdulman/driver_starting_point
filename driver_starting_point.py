import csv
from math import radians, cos, sin, asin, sqrt

def getClosestStartingPoint(starting_points, lat, lon):
    distances = []
    for starting_point in starting_points:
        distances.append(haversine(starting_point["starting_point_latitude"], starting_point["starting_point_longtitude"], lat, lon))

    min_distance = min(distances)
    index = distances.index(min_distance)

    res = {
        'min_distance': min_distance,
        'starting_point': starting_point,
        'other_points': get_other_points(starting_points, index)
    }
    return res

def get_other_points(starting_points, index):
    other_points = []
    i = 0
    for starting_point in starting_points:
        if index != i:
            other_points.append(starting_point)
        i+=1
    return other_points

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

driver_starting_points = []
with open('all_driver_starting_points.csv') as csvfile:
   readCSV = csv.reader(csvfile, delimiter=',')
   count = 0
   for row in readCSV:
       if count == 0:
           count += 1
           continue
       driver_starting_point = {
           'metro_name': row[0],
           'SP_metro_id': row[1],
           'starting_point_id': row[2],
           'starting_point_latitude': row[3],
           'starting_point_longtitude': row[4],
           'percentage': row[-1]
       }
       driver_starting_points.append(driver_starting_point)

driver_infos = []
with open('driver_info.csv') as csvfile:
   readCSV = csv.reader(csvfile, delimiter=',')
   count = 0
   for row in readCSV:
       if count == 0:
           count += 1
           continue
       driver_info = {
           'user_id': row[0],
           'metro_id': row[1],
           'latitude': row[2],
           'longtitude': row[3],
           'rating': row[4],
       }
       driver_infos.append(driver_info)

metro_ids= []
#find distinct metro ids by driver
for driver in driver_infos:
    try:
        metro_ids.index(driver["metro_id"])
    except:
        metro_ids.append(driver["metro_id"])



# TODO: loop this metro ids
results = []

for metro_id in metro_ids:
    metro_driver_infos = []
    metro_starting_points = []
    starting_point_percentages = []
    # TODO: filter driver_infos and driver_starting_points by the metro id
    for d in driver_infos:
        if d["metro_id"] == metro_id:
            metro_driver_infos.append(d)

    for dsp in driver_starting_points:
        if dsp['SP_metro_id'] == metro_id:
            metro_starting_points.append(dsp)
            starting_point_percentage ={
                'starting_point_id': dsp['starting_point_id'],
                'defined_percentage': dsp['percentage'],
                'filled_percentage': 0
            }
            starting_point_percentages.append(starting_point_percentage)

driver_count = len( metro_driver_infos )
one_driver_percentage = float( (1 / driver_count) * 100 )

for metro_driver_info in metro_driver_infos:
    closest_starting_point = {}
    isFoundClosestPlace = False

    closest = metro_starting_points
    while isFoundClosestPlace == False:
        closest_starting_point = getClosestStartingPoint( closest, metro_driver_info["latitude"],
                                                          metro_driver_info["longtitude"] )
        closest = closest_starting_point["other_points"]
        for starting_point_percentage in starting_point_percentages:
            if starting_point_percentage["starting_point_id"] == closest_starting_point["starting_point"][
                "starting_point_id"]:
                if metro_driver_info["rating"] != 5 and len( closest ) > 0 and float(
                        starting_point_percentage["filled_percentage"] ) >= float(
                        starting_point_percentage["defined_percentage"] ):
                    isFoundClosestPlace = False
                else:
                    starting_point_percentage["filled_percentage"] += one_driver_percentage
                    isFoundClosestPlace = True

        result = {
            'metro_driver_info': metro_driver_info,
            'closest_starting_point': closest_starting_point
        }
        results.append( result )

print(results)

