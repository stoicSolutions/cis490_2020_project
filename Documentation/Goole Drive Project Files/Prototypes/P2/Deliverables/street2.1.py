#! python3
import os
import re
import urllib.request
import random
import sys
import math
import shutil
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
#IMPORTANT: Put this script in the same directory as your GPX Files.
#==========================================================================================
# -----------------------------------    Step #1   ---------------------------------------- 
#==========================================================================================
#Path where you want Image Directories created.
BASE_SAVE_PATH = r"C:\Users\User\Pictures\Saved Pictures\TrashTrackerImages"
#==========================================================================================
# -----------------------------------    Step #2   ---------------------------------------- 
#==========================================================================================
#Google API Key
API_KEY = "&key=" + "AIzaSyD1FsP5missPGqStLlADBaqgIOTma45HM4"
#==========================================================================================
# -----------------------------------    Step #3   ---------------------------------------- 
#==========================================================================================
#Directory where your GPX Files are stored
BASE_PATH = r"C:\Users\User\Desktop\StoicK\GPXRoutes"
#==========================================================================================
#Holds all the filenames in the BASE_PATH directory.
filenames = []
unprocessedFiles = []
SAVE_PATHS = []
processedDataDict = {}
SIZE = "1200x800"   # currently limited to 600x600. Upgrade to Premium plan for higher resolution.

#Searches your specified BASE_PATH folder for .gpx files and adds them to filenames array.
def gatherGPXFiles():
	for entry in os.listdir(BASE_PATH):
		if os.path.isfile(os.path.join(BASE_PATH, entry)):
			if ".gpx" in entry:			
				filenames.append(entry)

#Creates a 'Processed' directory inside your BASE_PATH folder to store already processed .gpx files
def createProcessedDirectory():
	isDir = os.path.isdir(BASE_PATH+"\\Processed")
	if(isDir):
		print("Processed directory already exists.")
	else:
		os.mkdir(BASE_PATH)
		print("Processed directory created at : " + BASE_PATH+"//Processed.")

#Iterates through all .gpx files found in your specified BASE_PATH folder and allows you
#to create separate directories for each gpx file (answering [y]es), batch set them all to your BASE_SAVE_PATH (answering 'exit'),
#or set some to BASE_SAVE_PATH and some to separate directories (saying [n]o to the prompt).
def createSeparateDirectories():
	i = 0
	print("***Using Exit will set all GPX file to export to BASE_SAVE_PATH \n***Yes will create a directory in BASE_SAVE_PATH\\GPX_FILE_NAME \n***No will set a single GPX file to export to BASE_SAVE_PATH")
	while i < len(filenames):
		userInput = input("Create Directory for: " +filenames[i] +"? (y,n, or exit)" + "\n")
		if userInput == 'y' or userInput == 'Y':
			try:
				tempDir = filenames[i]
				tempDir = tempDir[0:-4]
				os.mkdir(BASE_SAVE_PATH+"\\"+tempDir)
				SAVE_PATHS.append(BASE_SAVE_PATH+"\\"+tempDir)
				print("Directory: " + tempDir + " created.\n")
				i+=1
			except:
				SAVE_PATHS.append(BASE_SAVE_PATH+"\\"+tempDir)
				print("Directory Already Exists!")
				i+=1
		elif userInput == 'n' or  userInput == 'N':
			print("No Directory Created for: " + filenames[i]+" using the BASE_SAVE_PATH: "+ BASE_SAVE_PATH + "\n")
			SAVE_PATHS.append(BASE_SAVE_PATH)
			i+=1
		elif userInput == 'exit':
			while i < len(filenames):
				print("No Directory Created for: " + filenames[i]+" using the BASE_SAVE_PATH: "+ BASE_SAVE_PATH + "\n")
				SAVE_PATHS.append(BASE_SAVE_PATH)
				i+=1
			break
		else:
			print("Invalid choice")

#For determining the bearing -----------------------------------------------
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.

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
    # from -180 to + 180 which is not what we want for a compass bearing
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
	print("Exporting " + file_name1 + " to " + save_path + ".")
    #do for -90 degrees
	location2 = "&location=" + address
	head2 = "&heading=" + heading2
	url2 = base + location + head2 + pitch + API_KEY	
	file_name2 = address + "_A2"+".jpg"#A2 = angle two which is the left side of street
	urllib.request.urlretrieve(url2, os.path.join(save_path, file_name2))
	print("Exporting " + file_name2 + " to " + save_path + ".")

def fetchPictures(GPX_FILE_NAME, SAVE_PATH):
	GPX_FILE = open(GPX_FILE_NAME).read()
	# parse gpx file for coordinates
	matches = re.findall('<trkpt lat="([-0-9\.]+)" lon="([-0-9\.]+)">', GPX_FILE)
	processedDataDict[GPX_FILE_NAME] = len(matches)
	# create array of coordinates
	coordinates = [lat + ',' + lon for lat, lon in matches]
	# ==========================================================================================================

	print("Processing... "+ GPX_FILE_NAME)

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
			
			#print(adjustedHeading1)
			#print(adjustedHeading2)
			getStreet(coordinates[i], SAVE_PATH,adjustedHeading1, adjustedHeading2)
			#sys.stdout.write("\r" + "[" + str(i) + " / " + str(amount - 1) + "] " + "Location: " + coordinates[i])
			#sys.stdout.flush()
	
	print(" \n Finished processing "+GPX_FILE_NAME)
	
def printStats():
	for gpxFiles,points in processedDataDict.items():
		gpxName = gpxFiles
		numImages = int(points) * 2
		print("File: " + gpxFiles, " had " + str(points) + " coordinates. It should have produced approximately " + str(numImages) + " Images.")

#Runs the script for each .gpx file, allowing you to confirm filename and save path or skip a file.
#Fetches the pictures from Google Street View
#Moves .gpx file to PROCESSED_PATH, assumes you have created 'Processed' Directory inside your BASE_PATH folder.
def runScript():
	createProcessedDirectory()
	gatherGPXFiles()
	createSeparateDirectories()

	i = 0;
	while i < len(filenames):
		userInput = input("Begin Processing GPX File: " + filenames[i] + "? Images will be exported to: " + SAVE_PATHS[i] + "([y]es, [s]kip, exit)\n")
		if userInput == 'y' or userInput == 'Y':
			try:
				fetchPictures(filenames[i],SAVE_PATHS[i])
				shutil.move(BASE_PATH+"\\"+filenames[i], BASE_PATH+"\\Processed")
				i += 1
			except:
				print("An error has occurred! The file will be marked as UNPROCESSED! Please manually check directories.") 
				unprocessedFiles.append(filenames[i])
				i += 1
		elif userInput == 's' or userInput == 'S':
			print("GPX File: " + filenames[i] + " will not be processed!")
			unprocessedFiles.append(filenames[i])
			i += 1
		elif userInput == 'exit':
			while i < len(filenames):
				unprocessedFiles.append(filenames[i])
				i+=1
			break;
		else:
			print("Invalid Input")
			
	print("=======================================================")
	print("      The following files have NOT been processed      ")
	print("\n".join(unprocessedFiles))
	print("=======================================================")
	print("               Script Running Data                     ")
	print("=======================================================")
	printStats()
	print("=======================================================")
			

runScript()
