from tutorial.mturk_client import mturk
import os

root = "/Users/alexwarstadt/Workspace/turktools/tutorial/"

for file in os.listdir(os.path.join(root, "my_questions")):

    question = open(name=os.path.join(root, "my_questions", file), mode='r').read()
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