=========================
Google App for Earthquakedata
=========================

-------
Warning
-------
Still in development needs lot of optimizations try it on your own risk

----------
Description
----------
Technologies: Python, Google Storage
Descriptions:
Implemented the earthqauke data visualisation and simple crud operations on the google cloudsql

Following steps are used to install the python for the Project. (Please install python 2.7.x not 3.4.X)
1. Install python 2.7.X, you can download python from https://www.python.org/downloads/
2. Get pip for the python 2.7.X, follow the instructions on https://pip.pypa.io/en/latest/installing.html to get pip.
3. Using pip you can install the required packages (pip install <module>)

To get started with Google Cloud follow the below steps:
1. Install the python client library for the google cloud, you can do this using the following command 
   pip install --upgrade google-api-python-client
   For more instructions follow the link https://developers.google.com/api-client-library/python/start/installation

2. Create an account at https://cloud.google.com/
3. Click on FreeTrail and fill the required details, click on accept and start free trail.
4. Click on create a project, give a project name and then click create. There are two cloud storage APIs XML API and JSON API.
   The guidelines provided here are for the JSON API. You can play with XML API as well if you wish to.
5. In the sidebar on the left click APIs & auth and then click on the Enabled APIs tab and make sure to see Google Cloud Storage JSON API is added 
   in there.  If you do not see it in there, select the API from the list of APIs, then select the Enable API button for the API.
6. In the side bar on the left click credentials. Click on the Create new client ID. Select installed application radio button and then click on
   configure consent screen. Enter a product name and then click on save.
7. You get a pop up again, click on installed application, installed application type - other. Click on Create Client ID.
8. You can see Clent ID and secret are created and you can click on Download JSON which downloads a JSON file (which you need it later).
9. On the left panel, click on storage -> cloud storage -> Storage Browser.
10. Click on create Bucket button. (Read here for info. about buckets and objects - https://cloud.google.com/storage/docs/overview )
11. Give the Bucket name and click on create, which creates a bucket to store your objects. Go ahead and create few objects or folders and play with it.

For more reading about JSON API - https://cloud.google.com/storage/docs/json_api/


