#! python3
import sys
import os
import random as ran
import datetime
import pymysql

#Connection Details
dbEndPoint = 'AWSEndpoint'
dbUserName = "aUserName"
dbPassword = "apassword"
dbName = "innodb"
dbCharset = 'utf8mb4'
cursorType = pymysql.cursors.DictCursor

#Create connection object
connection = pymysql.connect(host = dbEndPoint, password = dbPassword, db = dbName, user = dbUserName,port = 3306, charset = dbCharset, cursorclass = cursorType)

#Database format is as follows:
#ID, LAT, LONG ,RATING, NUM, DATE, ID is omitted from insert because DB is set to auto increment

#Location of Data file from ML server
BASE_SAVE_PATH = r"C:\Users\User\Desktop\StoicK"

#Dictionary to hold coordinates. It is useful because dictionaries only hold unique values.
#Because our raw data file contains two entries for each coordinate pair (Angle1 & Angle2) we can combine duplicate pairs.
#Adding each their litter_counts together to get a single litter_count for two images.
coordDict = {}

#Open raw data file
with open(BASE_SAVE_PATH+"\\"+"SanMarcosData.txt", "r") as f:
	#iterate through each line
	for line in f:
		#Lines are created as CSV so split them into each variable. Casting rank and count to ints for manipulation
		#and trimming the newline character off date.
		lat,long,rank,count,date = line.split(",")
		rank = int(rank)
		count = int(count)
		date = date.rstrip()
		#Combine lat and long into a single key
		key = lat + "," + long
		#If the key exists: add the current lines count value to the existing keys count
		#also update the existing keys kab_rank to reflect the new count value.
		if key in coordDict.keys():
			#print(line,coordDict[key],count)
			coordDict[key][1] += count
			if coordDict[key][1] >= 0 and coordDict[key][1] <= 2:
				coordDict[key][0] = 1
			elif coordDict[key][1] > 2 and coordDict[key][1] <= 5:
				coordDict[key][0] = 2
			elif coordDict[key][1] > 5 and coordDict[key][1] <=8:
				coordDict[key][0] = 3
			elif coordDict[key][1] > 8:
				coordDict[key][0] = 4
		else:
			coordDict.update({key:[rank,count,date]})
#Debug code
"""
count = 0
for x,y in coordDict.items():
	lat,long = x.split(",")
	
	print(count,lat,long,y[0],y[1],y[2])
	count += 1
"""
#Using PyMySQL connection object, create a cursor and for each item in the dictionary
#stage it to be committed to the database.
try:
	with connection.cursor() as cursor:
		for x,y in coordDict.items():
			lat,long = x.split(",")
			rank = y[0]
			count = y[1]
			date = y[2]
			sql = "INSERT INTO `SanMarcos` (`latitude`,`longitude`,`kab_rank`,`litter_count`,`date_taken`) VALUES (%s,%s,%s,%s,%s)"
			print(f"Running Query: INSERT INTO `SanMarcos` ('latitude','longitude','kab_rank','litter_count','date_taken') VALUES ({lat},{long},{rank},{count},{date})")
			cursor.execute(sql, (lat,long,rank,count,date))
	# connection is not autocommit by default. So you must commit to save your changes.
	connection.commit()
		
finally:
    connection.close()


