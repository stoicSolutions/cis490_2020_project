import os
import re
import urllib.request
import random
import sys
import math
# Create a route from:
# https://www.plotaroute.com/routeplanner
#

#
# Purpose: This is the current updated version of the street view image pulling script
# that will calculate heading and then pull the appropriate LEFT and RIGHT images.
# Given that it will be pulling the LEFT image and the RIGHT image at the exact same
# coordinates, we have made the file naming convention as follows:
#       file ending in "A1" = angle 1 which  is right side view of 360 image
#       file ending in "A2" = angle 2 which is left side of 360 image

#IMPORTANT: This is currently using python 3
GPX_FILE = open('Prototype1Route.gpx').read()
SAVE_PATH = r"C:\Users\Jerry Compton\Desktop\testing_local\Prototype1Images"
API_KEY = "&key=" + "API_KEY_GOES_HERE"

SIZE = "1200x800"   # currently limited to 600x600. Upgrade to Premium plan for higher resolution.

#For determining the bearing -----------------------------------------------
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
#----------------------------------------------------------------------

# Grab all of the "trkpt" elements
def getStreet(address, save_path, heading1, heading2):
    base = "https://maps.googleapis.com/maps/api/streetview?size=" + SIZE
    pitch = "&pitch=-20" #this is the tilt of the camera. 90 == stright up; -90 == straight down... so -20 should be good
    #do for +90 degrees
    location = "&location=" + address
    head = "&heading=" + heading1
    url = base + location + head + pitch + API_KEY

    file_name1 = address + "_A1"+".jpg"#A1 = angle one which  is right side of street
    urllib.request.urlretrieve(url, os.path.join(save_path, file_name1))
    
    #do for -90 degrees
    location2 = "&location=" + address
    head2 = "&heading=" + heading2
    url2 = base + location + head2 + pitch + API_KEY

    file_name2 = address + "_A2"+".jpg"#A2 = angle two which is the left side of street
    urllib.request.urlretrieve(url2, os.path.join(save_path, file_name2))

# parse gpx file for coordinates
matches = re.findall('<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">', GPX_FILE)

# create array of coordinates
coordinates = [lat + ',' + lon for lat, lon in matches]

# ==========================================================================================================

print('Running script ...')

start = 0
amount = len(coordinates)

for i in range(start, amount):
    
    latLon = coordinates[i].split(",")
    #sys.stdout.write(latLon[0] + latLon[1] + "\n")
    if i == 0:
        prev = [float(latLon[0]),float(latLon[1])]
    
    if i >= 1:
        curr = [float(latLon[0]),float(latLon[1])]
        currHeading = calculate_initial_compass_bearing(prev,curr)
        heading1 = currHeading+90#right side of street heading
        heading2 = currHeading-90#left side of street heading
        
        if heading1 > 360:
          heading1 = heading1 % 360

        if heading2 < 0:
          heading2 = heading2 + 360

        adjustedHeading1 = str(round(heading1, 2))
        adjustedHeading2 = str(round(heading2, 2))

        
        #set prevs
        prev[0] = float(latLon[0])
        prev[1] = float(latLon[1])
        
        print(adjustedHeading1)
        print(adjustedHeading2)
        getStreet(coordinates[i], SAVE_PATH,adjustedHeading1, adjustedHeading2)
        #sys.stdout.write("\r" + "[" + str(i) + " / " + str(amount - 1) + "] " + "Location: " + coordinates[i])
        #sys.stdout.flush()





print('\n Script completed ...')
