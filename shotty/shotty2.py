import boto3
import click
session2=boto3.Session(profile_name='shotty2')
ec2=session2.resource('ec2')
#@group.instances()
@click.command()
@click.option('--project',default=None,help="Only instances for project(tag Project:<name>)")
def list_instances(project):
    "List all instances"
    if project:
        filters=[{'Name':'tag:project','Values':['snapanalyzer']}]
        instances=ec2.instances.filter(Filters=filters)
    else:
        instances=ec2.instances.all()

    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        print(i.id,' ',i.instance_type,' ',i.state['Name'],' ',i.public_dns_name,' ',i.placement['AvailabilityZone'],' ',tags.get('project','<no project>'))

    return

if __name__=='__main__':
    list_instances()
