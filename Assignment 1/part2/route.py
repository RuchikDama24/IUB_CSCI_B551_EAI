#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Ayush Sanghavi sanghavi, Vighnesh Kolhatkar vkolhatk, Ruchik Dama rdama
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
import sys
import sys
import pandas as pd
import math
import heapq as hq


def successors(city,roads):
    city_list=[]
    city_1=roads.city1.values.tolist()
    city_2=roads.city2.values.tolist()
    if city in city_1:
        cities_total=roads[roads.city1==city]
        for i in cities_total.values.tolist():
            i.remove(city)
            i.append(1)
            city_list.append(i)
            #print(city_list)
        #print(city_list)
        #print(cities_total)
    if city in city_2:
        cities_total_1=roads[roads.city2==city]
        for i in cities_total_1.values.tolist():
            i.remove(city)
            i.append(1)
            city_list.append(i)
        #print(cities_total_1)
    #print(city_list)
    return city_list

def segment_heur(max_segment , haversine_dist):
    return max_segment/ haversine_dist


def distance_heur(city1, city2, city_gps):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    for i in city_gps[city_gps.city == city1].values.tolist():
        lon1 = math.radians(float(i[2]))
        lat1 = math.radians(float(i[1]))
    for i in city_gps[city_gps.city == city2].values.tolist():
        lon2 = math.radians(float(i[2]))
        lat2 = math.radians(float(i[1]))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 3956

    # calculate the result
    return c * r


def time_heur(haversine_dist,max_speed):
    return haversine_dist/max_speed


def probability_heur(haversine_dist):
    return haversine_dist * 0.00001


def find_probability(highway_prob, highway_miles):
    inter_mile = 0
    noninter_mile = 0
    if "I-" ==  highway_prob[:2]:
        inter_mile += highway_miles
    else:
        noninter_mile += highway_miles
    inter_probability = inter_mile * 0.00001
    noninter_probability = noninter_mile * 0.00002

    return float(inter_probability + noninter_probability)




def get_route(start, end, cost):

    """
    Find shortest driving route between start city and end city
    based on a cost function.
    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-expected-accidents": a float indicating the expected accident count on the route taken
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    city_gps = pd.read_csv('city-gps.txt', sep=" ", header=None)
    city_gps.columns = ["city", "latitude", "longitude"]
    city_gps.latitude.astype(float)
    city_gps.longitude.astype(float)

    roads = pd.read_csv('road-segments.txt', sep=" ", header=None)
    roads.columns = ["city1", "city2", "length", "speed", "highway"]
    roads.speed = roads.speed.astype(int)

    city1_unique = roads.drop_duplicates(subset=['city1'])
    city2_unique = roads.drop_duplicates(subset=['city2'])
    city1_unique = city1_unique.city1
    city2_unique = city2_unique.city2


    city1_2 = pd.concat([city1_unique, city2_unique])
    city1_2 = pd.DataFrame(city1_2)
    city1_2.columns = ["city"]
    city_gps = pd.concat([city_gps, city1_2], axis=0).drop_duplicates().reset_index(drop=True)

    # https://stackoverflow.com/questions/21317384/pandas-python-how-to-concatenate-two-dataframes-without-duplicates
    # https://datatofish.com/reset-index-pandas-dataframe/
    city_gps.drop(city_gps[city_gps['city'].duplicated()].index, inplace=True)
    city_gps.duplicated().sum()
    city_gps = city_gps.reset_index(drop=True)
    city_gps.fillna(0, inplace=True)

    max_speed = max(roads.speed)
    max_segment = max(roads.length)

    curr_state = start
    route_taken = []
    explored = []

    if (cost == 'segments'):
        fringe = []
        hq.heapify(fringe)
        hq.heappush(fringe, (0, 0, 0, 0, 0, [], start))
        while len(fringe) > 0:
            (cost_priority, total_segments, total_miles, total_hours, total_expected_accidents, route_taken, curr_state) = hq.heappop(fringe)
            explored.append(curr_state)
            for (city2, miles, speed, highway, segment) in successors(curr_state, roads):
                total_expected_accidents += find_probability(highway, miles)
                hours = miles / speed

                if city2 == end:
                    total_miles += miles
                    route_taken += [city2]
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    return {"total-segments": len(route_taken),
                            "total-miles": total_miles,
                            "total-hours": total_hours,
                            "total-expected-accidents": total_expected_accidents,
                            "route-taken": route_taken}

                elif (city2) in explored:
                    continue

                else:
                    explored.append(city2)
                    total_miles += miles
                    route_taken += [city2]
                    total_segments += segment
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)

                    haversine_dist = distance_heur(curr_state, end, city_gps)
                    cost_priority = segment_heur(max_segment, haversine_dist) + total_segments

                    hq.heappush(fringe, (cost_priority, total_segments, total_miles, total_hours, total_expected_accidents, route_taken, city2))

    if(cost == 'distance'):
        fringe = []
        hq.heapify(fringe)
        hq.heappush(fringe, (0, 0, 0, 0, [], start))
        while len(fringe) > 0:
            (cost_priority, total_miles, total_hours, total_expected_accidents, route_taken, curr_state ) = hq.heappop(fringe)
            explored.append(curr_state)
            for (city2, miles, speed, highway, segment) in successors(curr_state, roads):
                total_expected_accidents += find_probability(highway, miles)
                hours = miles/speed
                if city2 == end:
                    total_miles += miles
                    route_taken += [city2]
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    return {"total-segments": len(route_taken),
                            "total-miles": total_miles,
                            "total-hours": total_hours,
                            "total-expected-accidents": total_expected_accidents,
                            "route-taken": route_taken}

                elif (city2) in explored:
                    continue

                else:
                    total_miles += miles
                    #print(total_miles)
                    #print(city2)
                    cost_priority = distance_heur(curr_state, end, city_gps) + total_miles
                    #route_taken += city2
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    hq.heappush(fringe, (cost_priority, total_miles , total_hours , total_expected_accidents, route_taken + [(city2, highway)], city2))

    if (cost == 'time'):
        fringe = []
        hq.heapify(fringe)
        hq.heappush(fringe, (0, 0, 0, 0, [], start))
        while len(fringe) > 0:
            (cost_priority, total_hours, total_miles, total_expected_accidents, route_taken, curr_state) = hq.heappop(fringe)
            explored.append(curr_state)
            for (city2, miles, speed, highway, segment) in successors(curr_state, roads):
                total_expected_accidents += find_probability(highway, miles)
                hours = miles / speed
                if city2 == end:
                    total_miles += miles
                    route_taken += [city2]
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    return {"total-segments": len(route_taken),
                            "total-miles": total_miles,
                            "total-hours": total_hours,
                            "total-expected-accidents": total_expected_accidents,
                            "route-taken": route_taken}

                elif (city2, miles, speed, highway) in explored:
                    continue
                else:
                    total_miles += miles
                    haversine_dist = distance_heur(curr_state, end, city_gps)
                    cost_priority = time_heur(haversine_dist, max_speed) + total_hours
                    # route_taken += city2
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    hq.heappush(fringe,(cost_priority, total_hours, total_miles, total_expected_accidents, route_taken + [(city2, highway)], city2))


    if (cost == 'safe'):
        fringe = []
        hq.heapify(fringe)
        hq.heappush(fringe, (0, 0, 0, 0, [], start))
        while len(fringe) > 0:
            (cost_priority, total_expected_accidents, total_miles, total_hours, route_taken, curr_state) = hq.heappop(fringe)
            explored.append(curr_state)
            for (city2, miles, speed, highway, segment) in successors(curr_state, roads):
                total_expected_accidents += find_probability(highway, miles)
                hours = miles / speed
                if city2 == end:
                    total_miles += miles
                    route_taken += [city2]
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    return {"total-segments": len(route_taken),
                            "total-miles": total_miles,
                            "total-hours": total_hours,
                            "total-expected-accidents": total_expected_accidents,
                            "route-taken": route_taken}

                elif (city2) in explored:
                    continue
                else:
                    total_miles += miles
                    haversine_dist = distance_heur(curr_state, end, city_gps)
                    cost_priority = probability_heur(haversine_dist) + total_expected_accidents
                    # route_taken += city2
                    total_hours += hours
                    total_expected_accidents += find_probability(highway, miles)
                    hq.heappush(fringe, (cost_priority, total_expected_accidents, total_miles, total_hours, route_taken + [(city2, highway)], city2))

    """route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    """
# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))
    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])
