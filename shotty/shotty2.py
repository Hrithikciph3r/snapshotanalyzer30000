import boto3
import click
session2=boto3.Session(profile_name='shotty2')
ec2=session2.resource('ec2')
def filter_inst(project):
    instances=[]
    if project:
        filters=[{'Name':'tag:project','Values':[project]}]
        instances=ec2.instances.filter(Filters=filters)
    else:
        instances=ec2.instances.all()
    return instances

@click.group()
def instances():
    "command for instances"
@instances.command('list')
@click.option('--project',default=None,help="Only instances for project(tag project:<name>)")
def list_instances(project):
    "List all instances"
    instances=filter_inst(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        print(i.id,' ',i.instance_type,' ',i.state['Name'],' ',i.public_dns_name,' ',i.placement['AvailabilityZone'],' ',tags.get('project','<no project>'))

    return
@instances.command('stop')
@click.option('--project',default=None,help="Only to stop instances for project(tag project:<name>)")
def stop_instances(project):
    instances=filter_inst(project)
    for i in instances:
        print("Stopping ",i.id)
        i.stop()
    return
@instances.command('start')
@click.option('--project',default=None,help="Only to start instances for project(tag project:<name>)")
def start_instances(project):
    instances=filter_inst(project)
    for i in instances:
        print("Starting ",i.id)
        i.start()
    return
if __name__=='__main__':
    instances()
