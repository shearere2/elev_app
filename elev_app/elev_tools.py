import requests
import json
from geopy.distance import distance,lonlat
import numpy as np
import time

unit = 0.00027777777777 / 3.0 # 10 meters represented in decimal degrees

def find_elevation(lat:float, long:float) -> float:
    lat = float(lat)
    long = float(long)
    """Find the elevation of a coordinate

    Args:
        lat (float): Latitude
        long (float): Longitude

    Returns:
        float: Elevation in meters
    """
    '{0:.4f}'.format(lat)
    '{0:.4f}'.format(long)
    url = f'https://api.opentopodata.org/v1/ned10m?locations={lat},{long}'
    response = requests.get(url)
    string = response.content.decode()
    file = json.loads(string)
    time.sleep(1)
    '''I can be so specific on this return becuase of how
    specific I know the json format will be.'''
    return file['results'][0]['elevation']


def elevation_difference(start:tuple,end:tuple) -> float:
    start_elev = find_elevation(start[0],start[1])
    end_elev = find_elevation(end[0],end[1])

    if start_elev == None or end_elev == None: return 0
    return end_elev - start_elev # Represents meters that must be walked
#                                  uphill to get from point 1 to point 2

# FIRST TASK work out cumulative uphill travel between 2 points.
# MAYBE WORK TOWARDS WEBSITE WITH 2 FIELDS AND BUTTON FOR 

def summarize_journey(start:tuple,end:tuple) -> dict:
    """Summarize a linear journey between two coordinates
    (assumed that coordinates are linear from each other)

    Args:
        start (tuple): Starting coordinates
        end (tuple): Ending coordinates

    Returns:
        dict: Dictionary containing the following information:
        Cumulative uphill travel, cumulative downhill travel,
        total distance, total altitude change
    """
    if start == None or end == None:
        return {"Cumulative Uphill Travel":0,"Cumulative Downhill Travel":0,
            "Total Distance":0,"Total Altitude Change":0}
    start = (float(start[0]),float(start[1]))
    end = (float(end[0]),float(end[1]))
    dist = float(distance(lonlat(*start), lonlat(*end)).meters)
    alt = float(elevation_difference(start,end))
    increments = ((dist%10.0)*unit) # Represents number of 10 meter increments between points
    uphill = 0; downhill = 0
    hyp_slope = (start[0] - end[0]) / (start[1] - end[1])
    y_intercept = start[0] - (hyp_slope * start[1])
    lat_line = np.arange(start[0],end[0],increments,dtype=float) # Doesn't include end[0]
    lon_line = np.arange(start[1],end[1],increments,dtype=float) # ^^^^^

    
    if len(lat_line) > len(lon_line):
        lon_line = np.array([])
        for i in range(len(lat_line)):
            lon_line = np.append(lon_line,(lat_line[i] - y_intercept) / hyp_slope)

    elif len(lat_line) < len(lon_line):
        lat_line = np.array([])
        for i in range(len(lon_line)):
            lat_line = np.append(lat_line,(lon_line[i]*hyp_slope) + y_intercept)

    lon_line = np.append(lon_line,end[1])
    lat_line = np.append(lat_line,end[0])

    steps = []
    for i in range(len(lat_line)-1):
        steps.append(elevation_difference((lat_line[i],lon_line[i]),
                                          (lat_line[i+1],lon_line[i+1])))
        
    for dif in steps:
        if dif>0: uphill = uphill + dif
        elif dif<0: downhill = downhill - dif
        

    return {"Cumulative Uphill Travel":uphill,"Cumulative Downhill Travel":downhill,
            "Total Distance":dist,"Total Altitude Change":alt}

def linked_summary(coords_list:list) -> dict:
    """Provide elevational summary of a journey that takes turns

    Args:
        coords_list (list): List of tuples (coordinates), each
        representing a point along the journey

    Returns:
        dict: Dictionary containing the following information:
        Cumulative uphill travel, cumulative downhill travel,
        total distance, total altitude change
    """
    dist = float(distance(lonlat(*coords_list[0]), lonlat(*coords_list[-1])).meters)
    alt = elevation_difference(coords_list[0],coords_list[-1])
    uphill = 0;downhill = 0
    for i in range(len(coords_list)-1):
        temp_dict = summarize_journey(coords_list[i],coords_list[i+1])
        uphill = uphill + temp_dict['Cumulative Uphill Travel']
        downhill = downhill + temp_dict['Cumulative Downhill Travel']
    return {"Cumulative Uphill Travel":uphill,"Cumulative Downhill Travel":downhill,
            "Total Distance":dist,"Total Altitude Change":alt}

if __name__ == "__main__":
    #change = elevation_difference((40,-79.8),(40.01,-79.9))
    #print(f'To get from point one to point two, you will have to go up {change} meters')

    # journey = summarize_journey((40.1125,-79.8899),(40.1223,-79.8193))
    # print(journey)
    print()