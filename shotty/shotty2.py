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
def cli():
    """shotty group instances"""
@cli.group("snapshots")
def snapshots():
    "comand for snapshots"
@snapshots.command('list')
@click.option('--project',default=None,help="Only snapshots for project(tag project:<name>)")
@click.option('--all','list_all',default=False,is_flag=True,help="List all the snapshots")
def list_snapshot(project,list_all):
    "List all snapshots"
    instances=filter_inst(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        for v in i.volumes.all():
            for s in v.snapshots.all():

                print(s.id,' ',v.id,' ',i.id,' ',s.state,' ',s.progress,' ',s.start_time.strftime("%c"),' ',tags.get('project','<no project>'))
                if s.state=='completed' and not list_all:break

    return



@cli.group("volumes")
def volumes():
    "command for volumes"
@volumes.command('list')
@click.option('--project',default=None,help="Only volumes for project(tag project:<name>)")
def list_volumes(project):
    "List all volumes"
    instances=filter_inst(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        for v in i.volumes.all():

            print(v.id,' ',i.id,' ',v.state,' ',i.public_dns_name,' ',str(v.size),' ',"GiB ",v.encrypted and "Encrypted" or "Not Encrypted",' ',tags.get('project','<no project>'))










@cli.group("instances")
def instances():
    "command for instances"

@instances.command('snapshots')
@click.option('--project',default=None,help="Creating snapshots(tag project:<name>)")
def create_snapshot(project):
    "create a snapshot of volumes"
    instances=filter_inst(project)
    for i in instances:
        i.stop()
        print("Stopping for {0}".format(i.id))
        i.wait_until_stopped()
        tags={t['Key']:t['Value'] for t in i.tags or []}
        for v in i.volumes.all():
            print("Snapshotting for {0}".format(v.id))
            v.create_snapshot(Description="ss for snapanalyzer30000")

        i.start()
        print("Starting for {0}".format(i.id))
        i.wait_until_running()
    print("Jobs done")
    return


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
@click.option('--project',default=None,help="Only to stop instances for project")
def stop_instances(project):
    "Only to stop instances for project"
    instances=filter_inst(project)
    for i in instances:
        print("Stopping ",i.id)
        i.stop()
    return
@instances.command('start')
@click.option('--project',default=None,help="Only to start instances for project")
def start_instances(project):
    "Only to start instances for project"
    instances=filter_inst(project)
    for i in instances:
        print("Starting ",i.id)
        i.start()
    return


if __name__=='__main__':
    cli()
