import boto3

class EC2:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')

    def getSecurityGroups(self):
        return self.ec2.describe_security_groups()
    def getInstances(self):
    	return self.ec2_resource.instances
