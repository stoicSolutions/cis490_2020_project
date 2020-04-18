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

## Future Enhancements

### Team
Chris B.
Adam H.
Matthew A.
Enrique J.
Brian R.
Jerry C.
Jordan M.
Connor M.
