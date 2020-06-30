import boto3
#import click
session2=boto3.Session(profile_name='shotty2')
ec2=session2.resource('ec2')
#@click.command()
def list_instances():
    for i in ec2.instances.all():
        print(i.id,' ',i.instance_type,' ',i.state['Name'],' ',i.public_dns_name,' ',i.placement['AvailabilityZone'])

    return

if __name__=='__main__':
    list_instances()
