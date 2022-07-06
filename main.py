from venv import create
import requests
import re
import json
from waypoints import get_way_points
import numpy as np

#url = 'https://opendata-download-metfcst.smhi.se/api/category/fwif1g/version/1/daily/geotype/point/lon/16/lat/58/data.json'
#x = requests.get(url)
#data = x.text
#transformed_data = json.loads(data)
#print(transformed_data["timeSeries"])

def create_url_from_coordinate(Lat, Long):
    return 'https://opendata-download-metfcst.smhi.se/api/category/fwif1g/version/1/daily/geotype/point/lon/' + Long + '/lat/' + Lat + '/data.json'

def get_met_fcst(Lat, Long):
    url = create_url_from_coordinate(Lat, Long)
    x = requests.get(url)
    data = x.text
    JsonData = json.loads(data)
    return JsonData["timeSeries"]

def extract_fwi_index_values(Fcst):
    FwiIndexIndex = 0
    FwiIndexList = []
    for Day in range(len(Fcst)):
        FwiIndex = Fcst[Day]["parameters"][FwiIndexIndex]['values'][0]
        FwiIndexList.append(FwiIndex)
    return FwiIndexList

def print_way_points(WayPoints):
    for wp in WayPoints:
        print(wp['name'])
        print(wp['fcst'])

def store_fwi_indices(WayPoint, FwiIndexList):
    WayPoint['fcst'] = FwiIndexList

def update_fcst():
    Waypoints = get_way_points()
    for wp in Waypoints:
        [Lat, Long] = wp['coord']
        Fcst = get_met_fcst(Lat, Long)
        FwiIndexList = extract_fwi_index_values(Fcst)
        store_fwi_indices(wp, FwiIndexList)
    return Waypoints

def transform_waypoints(WayPoints):
    FcstMatrix = []
    for wp in WayPoints:
        Fcst = wp['fcst']
        FcstMatrix.append(Fcst)
    return FcstMatrix 



if __name__ == "__main__":
    WayPoints = update_fcst()
    FcstMatrix = transform_waypoints(WayPoints)
    print(FcstMatrix)
