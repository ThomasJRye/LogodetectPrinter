import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import utils

def update_video():
    video_query = "select * from logograb_videos inner join logograb_video_analysis on logograb_videos.id = logograb_video_analysis.video_id where logograb_video_analysis.status = 'PROCESSING' and logograb_videos.created_at > '2023-01-08 00:00:00';"
    video_urls = execute(video_query)
    print(video_urls)

def update_logos():
    #query = "SELECT id,url FROM logograb_videos WHERE created_at > '2023-01-08 00:00:00'"
    #get all filenames in an S3 bucket
    logos = execute(query)

    #get all filenames in an directory
    logos = [f for f in os.listdir('/home/ubuntu/.hkt/logodetect/data/logos/') if os.path.isfile(os.path.join('/home/ubuntu/.hkt/logodetect/data/videos/', f))]
    print(logos)




def execute(query):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def connect():
    load_dotenv()
    
    #load database configuration
    config = {
            'host': os.getenv('db_host'),
            'user': os.getenv('db_user'),
            'password': os.getenv('db_password'),
            'database': os.getenv('db'),
            'port':  os.getenv('db_port')
        }
    
    try:
        #create connection to database
        connection = mysql.connector.connect(**config)

        if connection.is_connected():

            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)