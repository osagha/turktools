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

print "I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account"

question = open(name='/Users/alexwarstadt/Workspace/turktools/tutorial/questions.xml', mode='r').read()
new_hit = mturk.create_hit(
    Title='Is this Tweet happy, angry, excited, scared, annoyed or upset?',
    Description='Read this tweet and type out one word to describe the emotion of the person posting it: happy, angry, scared, annoyed or upset',
    Keywords='text, quick, labeling',
    Reward='0.15',
    MaxAssignments=1,
    LifetimeInSeconds=172800,  # 48 hours
    AssignmentDurationInSeconds=600,
    AutoApprovalDelayInSeconds=14400,  # 4 hours
    Question=question,
)
print "A new HIT has been created. You can preview it here:"
print "https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId']
print "HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)"
# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=
