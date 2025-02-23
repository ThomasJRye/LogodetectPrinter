"""Global utilities."""

# Standard library:
import os
import mysqlx

# Pip packages:
import numpy as np
import pandas as pd
from PIL import Image
from torchvision.transforms import functional as F
import torch
from typing import Tuple
import boto3
from dotenv import load_dotenv




def open_and_resize(path: str, image_resize: Tuple[int, int]) -> Image.Image:
    """Checks if image is valid and moves it to the GPU.

    :param path: path to image
    :param image_resize: tuple of two integers
    :return: resized PIL.Image
    """
    return Image.open(path).convert("RGB").resize(image_resize)


def image_to_gpu_tensor(image: Image.Image, device: str) -> torch.Tensor:
    """Checks if image is valid and moves it to the GPU.

    :param image: PIL.Image
    :param device: device to run op on
    :return:
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise Exception(
            "'predict' method takes a 3D image as input \
            of shape (H, W, 3). Instead got {}".format(
                image.shape
            )
        )
    return F.to_tensor(image).unsqueeze(0).to(device)


def clean_name(filename: str) -> str:
    """Clean file name

    :param filename: name of the file you want to clean.

    Example:
    >> ' '.join(sorted(set(''.join(list(set(brands))))))
    >> "& ' + - 1 2 3 4 ? a b c d e f g h i j kl m n
        o p q r s t u v w x y z \udcbc \udcc3 \udcfc"
    """
    name, extension = os.path.splitext(os.path.basename(filename))
    brand = name.split("_")[0]
    return brand.encode("ascii", "replace").decode()


def save_df(vectors, file_names, path, net_type="") -> None:
    """Save image vectors and brands stored in file
    names as pandas DataFrame. Only used for visualisation, e.g. in notebooks.

    :param vectors:
    :param file_names:
    :param path:
    :param net_type:
    :return:
    """
    vectors_list = [v for v in vectors]
    brands = [clean_name(n) for n in file_names]
    logos_df = pd.DataFrame({"brand": brands, "img_vec": vectors_list})
    logos_df.to_pickle(path + "{}.pkl".format(net_type))

def import_from_s3():
    # load environment variables from .env file
    load_dotenv()

    # access specific s3 bucket
    bucket_name = os.getenv('AWS_BUCKET')

    # create an S3 client
    s3 = boto3.client


def import_video():

    # load environment variables from .env file
    load_dotenv()

    # access specific s3 bucket
    bucket_name = os.getenv('AWS_BUCKET')

    # create an S3 client
    s3 = boto3.client('s3')

    # list all of the buckets in your account
    response = s3.list_buckets()
    #print(response)

    file_name = '/visua/20210927_TV2_Sportsnyhetene_2125.mp4'
    local_file_path = '/home/ubuntu/.hkt/logodetect/data/videos/'

    #response = s3.get_object(Bucket=bucket_name, Key='7801207_2021_05_27_VIK_MIF_2nd_Half_416444.mp4')

    #os.makedirs(os.path.dirname(local_file_path))

    s3.download_file(bucket_name, '7801207_2021_05_27_VIK_MIF_2nd_Half_416444.mp4', local_file_path + '7801207_2021_05_27_VIK_MIF_2nd_Half_416444.mp4')

    # list all the files in specific bucket
    #response = s3.list_objects(Bucket=bucket_name)

    print(response)



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
        connection = mysqlx.connector.connect(**config)

        if connection.is_connected():

            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)