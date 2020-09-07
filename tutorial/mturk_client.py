# Based on tutorial here: https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977
import boto3

credentials_file = open("/Users/alexwarstadt/Downloads/new_user_credentials.csv")
credentials_file.readline()
credentials_line = credentials_file.readline()
aws_access_key_id = credentials_line.split(",")[2]
aws_secret_access_key = credentials_line.split(",")[3]

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
                     aws_access_key_id=aws_access_key_id,
                     aws_secret_access_key=aws_secret_access_key,
                     region_name='us-east-1',
                     endpoint_url=MTURK_SANDBOX  # comment out this line to connect to live MTurk marketplace
                     )