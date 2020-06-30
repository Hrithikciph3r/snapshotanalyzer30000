import boto3
if __name__=='__main__':
    session2=boto3.Session(profile_name='shotty2')
    ec2=session2.resource('ec2')
    for i in ec2.instances.all():
        print(i)
