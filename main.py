__author__ = 'samvarankashyap'
"""
The working copy of the application is running at the following urls :
cloudcomputing1-970.appspot.com
cloudcomputing1-970.appspot.com/upload for upload functionality
"""
from bottle import Bottle
from bottle import route, request, response, template, HTTPResponse
import os
import MySQLdb
import time
import cloudstorage as gcs
from test.assignment2 import *
from google.appengine.api import app_identity
import re
import datetime
import json
from collections import defaultdict
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

bottle = Bottle()

@bottle.route('/')
def hello():
    """Main function responsible for home page calculating the time to insert """
    #variable to determine the where app is running
    env = os.getenv('SERVER_SOFTWARE')
    main_string = "Time to Insert data ::"
    try:
        #getting the default bucket name from the application environment
        bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
        #file_name = "/"+bucket_name+"/all_month.csv"
        #creating the file name including the path of the bucket
        file_name = "/"+bucket_name+"/demo-testfile.csv"
        #getting db connection according to the environment by calling get_connection object  
        db = get_connection(env)
        # creating cursor object to execute the queries
        cursor = db.cursor()
        #initialising the databases and the tables if not created with the ionitialise_dbfunction which returns current cursor 
        cursor = initialise_db(cursor)
        #starting the clock for calculate insert time
        s_time = time.time()
        # inserting data into the using the bucket
        insert_into_table(cursor,file_name)
        # commiting the changes 
        db.commit()
        # stopping the clock
        e_time = time.time()
        # calculating the time required to insert the data
        t_time = str(e_time-s_time)
        #getting all earthquakes greater than magnitude 5,4,3,2 
        mag_5 = len(get_eq_gr_mag(cursor ,5))
        mag_4 = len(get_eq_gr_mag(cursor ,4))
        mag_3 = len(get_eq_gr_mag(cursor, 3))
        mag_2 = len(get_eq_gr_mag(cursor, 2))
        # getting all the earthquakes of magnitude equal t0 5,4,3,2
        m_5 = len(get_eq_equal_mag(cursor,5))
        m_4 = len(get_eq_equal_mag(cursor,4))
        m_3 = len(get_eq_equal_mag(cursor,3))
        m_2 = len(get_eq_equal_mag(cursor,2))
        #getting the weekly earthequake count for magnitude 5,4,3,2
        rows_5 = filter_result(get_eq_equal_mag(cursor ,5))
        rows_4 = filter_result(get_eq_equal_mag(cursor ,4))
        rows_3 = filter_result(get_eq_equal_mag(cursor ,3))
        rows_2 = filter_result(get_eq_equal_mag(cursor ,2))
        result_string = rows_5+"<br>"+rows_4+"<br>"+rows_3+"<br>"+rows_2  
        # creating a formatted output string for displaying resilus as http response
        output = ""
        output += "<h3>"+main_string+str(t_time)+"</h3>"
        output += "<h3>Number of earthquakes greater than maginitude 5: "+str(mag_5)+"</h3>"
        output += "<h3>Number of earthquakes greater than maginitude 4: "+str(mag_4)+"</h3>"
        output += "<h3>Number of earthquakes greater than maginitude 3: "+str(mag_3)+"</h3>"
        output += "<h3>Number of earthquakes greater than maginitude 2: "+str(mag_2)+"</h3>"
        output += "<h3>Number of earthquakes equal to maginitude 5: "+str(m_5)+"</h3>"
        output += "<h3>Number of earthquakes equal to maginitude 4: "+str(m_4)+"</h3>"
        output += "<h3>Number of earthquakes equal to maginitude 3: "+str(m_3)+"</h3>"
        output += "<h3>Number of earthquakes equal to maginitude 2: "+str(m_2)+"</h3>"
        # returning the output by appending the results to it 
        return output+"<h3>Number of Earthquakes per each week of maginitude 5,4,3,2<br>"+result_string+"</h3>"
    except Exception as e:
        # printing the exception message to the logs if exists for debugging purpose
        return str(e)

def get_connection(type_of_con):
    """ This function is responsible for returning the appropriate environment object """
    try:
        #checking if the environment is google app engine or not
        if (type_of_con and type_of_con.startswith('Google App Engine/')):
            #creating the db connection by connecting it to the google app engine unix socket.
            db = MySQLdb.connect(unix_socket='/cloudsql/cloudcomputing1-970:mysql-server-1',user='root')
            #returning the database connection
            return db
        else:
            # if the environment is other thangoogle app engine it will try to connect with the local host with default username and password
            con = mdb.connect('localhost', 'root', 'root', 'test')
            return con
    except Exception as e:
        #prints the exception to the logs if there are any with a user defined message
        print "Connection to the database failed : "+str(e)

def initialise_db(cursor):
    """This function is to responsible for the initialisation the the database and tables """
    try:
        # creates database test if not exists
        result2 = cursor.execute('CREATE DATABASE IF NOT EXISTS test')
        # selects the database test to create tables
        result2 = cursor.execute('use test')
        # creates the schema for the earthquakes table if it doesnt exist
        result2 = cursor.execute('CREATE TABLE IF NOT EXISTS EARTHQUAKES (time TIMESTAMP,latitude DOUBLE PRECISION(15,7),longitude DOUBLE PRECISION(15,7),depth DOUBLE ,mag DOUBLE,magType varchar(255),nst VARCHAR(255),gap VARCHAR(255),dmin VARCHAR(255),rms VARCHAR(255),net varchar(255), id varchar(255),updated TIMESTAMP,place varchar(255),type varchar(255))')
        # empties the table earthquakes 
        result2 = cursor.execute("truncate EARTHQUAKES")
        # creates a primary key for the earthquakes function
        result2 = cursor.execute("ALTER TABLE EARTHQUAKES ADD PRIMARY KEY (id)");
    except Exception as e:
        #prints exception to the logs.
        print "Reinitialisation of the tables :: "+str(e)
    return cursor

def read_file(filename):
    """ Reads a file from the bucket object where file name is in format of the /bucket_name/file_name"""
    #opens the file 
    gcs_file = gcs.open(filename)
    content = ""
    #reads each line the and append it to content
    for line in gcs_file:
        content += line
    # returns the content
    return content    

def filter_result(result):
    """Takes the result of the rows as the input and filters it according to the week  """
    # creates the default dictionary 
    weeks_dic = defaultdict(int)
    result_string = ""
    # counts all the rows by the weeks number 
    for row in result:
        date = row[0]
        # gets the week number of the date
        week = get_week(date.year,date.month,date.day)
        month_week = "Month:"+str(date.month)+":week:"+str(week)
        weeks_dic[month_week]+=1
        print date,week
    #sorting the default dictionary according to week and magnitude for display purposes
    for key in sorted(weeks_dic):
        result_string += key+": "+str(weeks_dic[key])+"<br>"
    return result_string


def get_week(year, month, day):
    """ This function the retrive the week number from the year , month , and day """
    first_week_month = datetime.datetime(year, month, 1).isocalendar()[1]
    if month == 1 and first_week_month > 10:
        first_week_month = 0
    user_date = datetime.datetime(year, month, day).isocalendar()[1]
    if month == 1 and user_date > 10:
        user_date = 0
    return user_date - first_week_month+1

def insert_into_table(cursor,filename):
    """ function is responsible for inserting data into the table """
    #initialise the fields for inserting
    to_insert={}
    # opens the bucket object for reading 
    gcs_file = gcs.open(filename)
    try:
        for line in gcs_file:
            fields = line.split(",")
            if(fields[0]=="time"):
                continue
            else:
                #initialises all the fiels
                to_insert['time'] = fields[0]
                to_insert['latitude'] = float(fields[1])
                to_insert['longitude'] = float(fields[2])
                to_insert['depth'] = float(fields[3])
                to_insert['mag'] = float(fields[4])
                to_insert['magtype'] = fields[5]
                to_insert['nst'] = fields[6]
                to_insert['gap'] = fields[7]
                to_insert['dmin'] = fields[8]
                to_insert['rms'] = fields[9]
                to_insert['net'] = fields[10]
                to_insert['idn'] = fields[11]
                to_insert['updated'] = fields[12]
                to_insert['place'] = fields[13].replace("'","").replace("\"","")
                to_insert['type_of'] = fields[14].strip("\n")
                # creates the insert query to insert data
                query = create_insert(to_insert)
                #print query
                # excutes the query to insert data
                cur_r = cursor.execute(query)
    except Exception as e:
        print "Duplicate entries "+str(e)

def create_insert(to_insert):
    """Function responsible for creating the query """
    # formatting the time according to the mysql
    formated_time = format_time(to_insert['time'])
    formated_updated = format_time(to_insert['updated'])
    # create the query string
    query = "INSERT INTO EARTHQUAKES(time,latitude,longitude,depth,mag,magtype,nst,gap,dmin,rms,net,id,updated,place,type) VALUES("
    query += "'"+formated_time+"'"+","
    query += str(to_insert['latitude'])+","
    query += str(to_insert['longitude'])+","
    query += str(to_insert['depth'])+","
    query += str(to_insert['mag'])+","
    query += "'"+to_insert['magtype']+"'"+","
    query += "'"+to_insert['nst']+"'"+","
    query += "'"+to_insert['gap']+"'"+","
    query += "'"+to_insert['dmin']+"'"+","
    query += "'"+to_insert['rms']+"'"+","
    query += "'"+to_insert['net']+"'"+","
    query += "'"+to_insert['idn']+"'"+","
    query += "'"+formated_updated+"'"+","
    query += "'"+to_insert['place'].rstrip("\"")+"'"+","
    query += "'"+to_insert['type_of']+"'"+")"
    return query
    
def format_time(time_string):
    """ Function to format the time according to Mysql syntax """
    date = time_string.split("T")[0]
    time = time_string.split("T")[1]
    #2008-01-01 00:00:01
    return date+" "+time.split(".")[0]

def get_eq_gr_mag(cursor ,magnitude):
    """Query to get the earth quakes greater than a maginitude """
    cursor.execute("SELECT * FROM EARTHQUAKES WHERE mag >"+str(magnitude))
    rows = cursor.fetchall()
    return rows

def get_eq_equal_mag(cursor,magnitude):
    """Query to get the earth quakes equal to a  maginitude """
    cursor.execute("SELECT * FROM EARTHQUAKES WHERE mag ="+str(magnitude))
    rows = cursor.fetchall()
    return rows

@bottle.route('/upload')
def upload(name="User"):
    """ Function for displaying form on the upload page"""
    return template('upload_template', name=name)

@bottle.route('/doupload',  method='POST')
def doupload(time_taken=0):
    """ Function responsible for the upload action that is performed """
    # starting the clock to calculate upload time 
    start_time = time.time()
    # getting the default application bucket based on the app identity
    bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
    # formatting the file name for creation 
    filename = '/'+bucket_name+ '/demo-testfile.csv'
    # getting the data object of the uploaded csv file
    data = request.files.get('data')
    # reading the data 
    raw = data.file.read()
    # initialising retry parameters for the request
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    # creating file on the bucket
    gcs_file = gcs.open(filename,'w',content_type='text/plain',options={'x-goog-meta-foo': 'foo','x-goog-meta-bar': 'bar'},retry_params=write_retry_params)
    # writing the data to the bucket object
    gcs_file.write(raw)
    # closing the bucket object
    gcs_file.close()
    # getting the end time of upload
    end_time = time.time()
    # calculating the total time taken 
    time_taken = end_time-start_time
    #retuning the data to the download template 
    return template('doupload_template',time_taken=time_taken)


@bottle.route('/webinterface')
def webinterface():
    return template('webinterface')

@bottle.route('/querybuilder',  method='POST')
def query_builder():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #print request.forms.dict
        #print request.files.dict
        #print dir(request.files)
        posted_dict =  request.forms.dict
        #print posted_dict
        query = build_query(posted_dict) 
        #return json.dumps(posted_dict)
        data = execute_query(query)
        data = convert_to_json(data)
        #data = str(data)
        data = json.dumps(data)
        print type(data)
        print len(data)
        resp = HTTPResponse(body=data,status=200)
        return resp
    else:
        return 'This is a normal request'

def build_query(json_obj):
    query = "SELECT * FROM  EARTHQUAKES WHERE "
    param1 = ""
    param2 = ""
    if "parameter1" in json_obj:
        if json_obj["parameter1"][0] == "gt":
            param1 = ">"
        elif json_obj["parameter1"][0] == "eq":
            param1 = "="
        elif json_obj["parameter1"][0] == "lt":
            param1 = "<"
        elif json_obj["parameter1"][0] == "lte":
            param1 = "<="
        elif json_obj["parameter1"][0] == "gte":
            param1 = ">="
    if "magnitude" in json_obj:
        query += "mag "+param1+" "+json_obj["magnitude"][0]
    if "parameter2" in json_obj:
        if json_obj["parameter2"][0] == "and":
            param2 = "AND"
        if json_obj["parameter2"][0] == "or":
            param2 = "OR"
    if "location" in json_obj:
        if json_obj["location"][0]!="":
            query += " "+param2+" "+"place LIKE '"+json_obj["location"][0]+"'"
    #print query
    return query

def convert_to_json(data):
    all_objs = {}
    #time,latitude,longitude,depth,mag,magtype,nst,gap,dmin,rms,net,id,updated,place,type
    for x in data:
        json_obj={}
        json_obj["time"]=x[0].strftime("%d/%m/%Y %H:%M:%S")
        json_obj["latitude"]=x[1]
        json_obj["longitude"]=x[2]
        json_obj["depth"]=x[3]
        json_obj["mag"]=x[4]
        json_obj["magtype"]=x[5]
        json_obj["nst"]=x[6]
        json_obj["gap"]=x[7]
        json_obj["dmin"]=x[8]
        json_obj["rms"]=x[9]
        json_obj["net"]=x[10]
        json_obj["id"]=x[11]
        json_obj["updated"]=x[12].strftime("%d/%m/%Y %H:%M:%S")
        json_obj["place"]=x[13]
        json_obj["type"]=x[14].strip("\"")
        all_objs[x[11]]=json_obj
    print all_objs
    return all_objs
        
    
def execute_query(query):
    env = os.getenv('SERVER_SOFTWARE')
    db = get_connection(env)
    c = db.cursor()
    c.execute("use test")
    c.execute(query)
    data = c.fetchall()
    print data
    return data

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.'
