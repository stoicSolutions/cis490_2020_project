![logo](https://github.com/mower003/cis490_2020_project/blob/master/img/StoicSolutionsTextAboveLogoSmall.png) 

## San Marcos Litter Detection
#### CSUSM: Project Management & Practice
#### Instructor: Dr. Shaun-inn Wuu
#### Clients: Dr. Wesley Schultz & Dr. Kristin Stewart
#### Spring 2020 

## Project Outline
Building on fixIT's previous work the Stoic Solutions team was tasked with using their machine learning algorithm to process street images for the city of San Marcos.

## Guiding Questions

* How to collect latitude/longitude points throughout the city?
* Is it necessary to collect all four images from a panorama?
* Once we have the latitude/longitude files how should we process them?
* What information is relevant for the team creating the user interface?
* How do we get the data from the machine learning algorithm to the relational database?

## Things you will need
* Goole Street View API Key (For fetching images) [Google Cloud Platform](https://cloud.google.com/)
* AWS Account (For storing data in a database) [AWS](https://aws.amazon.com/)
* Access to TrashTracker EC2 Instance (For processing images with tensorflow)
* An account with plotaroute.com [Plotaroute](https://www.plotaroute.com/routeplanner)

## Implementation
#### How we collected coordinates
Using plotaroute we manually created routes throughout San Marcos. Plotaroute allows you to save these routes as a GPX file and download them. This is useful because we can then parse these files with a python script and pass those coordinates to Google Street View to collect images. Below is a sample route of the 78.
![78](https://github.com/mower003/cis490_2020_project/blob/master/img/ca78img.png)
A GPX File will look like the following picture:
![gpx](https://github.com/mower003/cis490_2020_project/blob/master/img/gpxSample.png)
These files can be parsed using our python script: 'street2.1.py' located in the Scripts folder.
#### Collecting Pictures
We decided that collected front and back images would not only be redundant, but add unnecessary difficulties, costs, and time to the project. Therefore, we opted to capture both the left and right images (sides of the street). This requires a route to have points greater than or equal to two so that a heading can be calculated. 
##### Street2.1.py Details
* Uses Python3
* Requires Google API Key to fetch images.
* Requires user to edit the script and set a BASE_PATH
* The script was designed to run on a large batch of GPX Files. It will prompt you as to whether you'd like to create individual directories for each GPX File ran, or if you'd like to store all the images in the BASE_PATH location.
* Should anything go wrong, it will output which GPX Files were successfully processed and which were unprocessed as well as moving processed ones to the 'Processed' folder (automatically created).
Below is a screenshot of the script running on a GPX File.
![street2.1.py](https://github.com/mower003/cis490_2020_project/blob/master/img/street2.1img.png)

##### Processing Images Using Machine Learning on the EC2 Server
* After the previous steps we had several batches of images (approx 4000 total).
* These were uploaded to the EC2 server and processed using the previously established machine learning algorithm.
* Minor adjustments to the previous groups script were made so that output was redirected to a text file rather than displaying it inside Jupyter Notebook. The script `Stoicsolutions_KABProcessor.ipynb` used to process the images is located in the /scripts folder of GitHub and also on the EC2 Server.
* Processing the images takes quite a long time. In our case, we had 4,216 images. The average processing time per picture was 6 seconds. Therefore, it took about 7 hours to process all our images (((6s * 4,216)/60)/60) = 7.027 hours). This is mentioned because we feel this data set is considered small. Future groups may be expected to gather larger data sets which will result in much longer processing times.
### fixIT Script & Output
![fixIt Script](https://github.com/mower003/cis490_2020_project/blob/master/img/fixITScriptImage.png)

### Stoic Solutions Script & Output
![Stoic Solutions Script](https://github.com/mower003/cis490_2020_project/blob/master/img/StoicSolutionScriptImage.png)

#### Processing Raw ML Output
* The next step in our solution involves collating data from multiple angles into a single point of data per coordinate pair. This is necessary because data from the ML process produces duplicate coordinate pairs for every angle. Not only do we want to remove duplicate coordinates but we want to sum the counted pieces of litter from each angle and assign a new KAB Rating based on the sum of the litter.
* This process was accomplished using the 'database.py' script. For every line in the raw ML text file it parses the line into its components (lat,lon,KAB_rating,litter_count,date). A dictionary or associative array is used where k(lat,lon) = v(KAB_rating,litter_count,date). This allows for only unique K,V pairs to exist. Any following line where K exists has its litter_count summed with the current lines litter_count and KAB_rating is adjusted accordingly.
* 4,216 unique images -> 4,216 lines of data  -> 2,108 unique points -> 2,108 rows of data in the database.
* PyMySQL was used to connect to our Amazon RDS instance and run queries to insert the refined data into the database. 
![database.py](https://github.com/mower003/cis490_2020_project/blob/master/img/databaseScript.png)
* If you wish to recreate our database, simply download the `SanMarcosData.txt` and `database.py` files. Modify the `BASE_SAVE_PATH`, and connection credentials in `database.py`. Run the script and it will populate your database with our data set. 

### Summary
* Using plotaroute.com we gathered GPX files for streets within the city of San Marcos.
* These GPX files were parsed for coordinates which were then passed to Google Street View where we captured pictures of the sides of the street.
* The pictures were then procssed using a previously established machine learning server and produced data in the form of (lat,lon,rating,litter_count,date).
* This data was further refined and then inserted into an AWS Relational Database so it can be used by the UI team.

## Future Enhancements - Automating route collection
* The most glaring deficiency in our solution is the method of gathering coordinate pairs to be passed to Google Street View. Manually plotting routes for a city is not scalable. Google provides no API solutions for traversing streets without knowing coordinates beforehand so a third party solution seems to be the only relevant way to solve this. 
* Automation of route collection would greatly improve the scalability, second only to speeding up ML processing.
* Unfortunately for us (but luckily for the next group) we came across a possible solution to this problem late into the semester.
* OSMnx provides many ways to interact with data gathered by volunteers and other data collection methods. Most importantly, it provides coordinate pairs of every street for a queried city. The below image was created using OSMnx. We have also included the OSMnx file titled `SMStreetCoords(OSMnx).txt` that contains street names and a list of coordinates for the graph as well as the `AllStreetsInACity.ipynb` script that was used to create these.
* It should be possible to use OSMnx to gather a list of streets and their coordinates, parse them using python, and then pass a list of coordinates to the Google Roads API (using Snap-to-Roads) to interpolate. This must be done because OSMnx coordinate pairs DO NOT map directly to those used by Google. However, Google Roads API can take approximate coordinate data and return a list of coordinates that represent valid locations within Street View. Using these, you can then query Google Street View to collect images similarly to how we have done.
* Here is a link to installing OSMnx and the site also has guides on how to use it.
![Link to installing OSMnx](https://geoffboeing.com/2017/02/python-getting-started/)
![OSMnx San Marcos](https://github.com/mower003/cis490_2020_project/blob/master/img/SanMarcosA.png)

### Team
Chris B. |
Adam H. |
Matthew A. |
Enrique J. |
Brian R. |
Jerry C. |
Jordan M. |
Connor M. |
