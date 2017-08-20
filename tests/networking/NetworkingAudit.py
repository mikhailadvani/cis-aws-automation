import unittest
from aws.api import EC2
from aws.entity import SecurityGroup

class NetworkingAudit(unittest.TestCase):
    def testSshNotOpenFromInternet(self):
        allSecurityGroups = self._getAllSecurityGroups()
        sshOpenSecurityGroups = self._filterSecurityGroupsWithProtocolPortOpenFromInternet(allSecurityGroups, 'tcp', 22)
        self.assertEqual([], sshOpenSecurityGroups, "Security group(s) with SSH allowed from Internet[vpcId:groupId]: %s. Recommendation: 4.1" % self._groupIdsVpcIds(sshOpenSecurityGroups))

    def testRdpNotOpenFromInternet(self):
        allSecurityGroups = self._getAllSecurityGroups()
        rdpOpenSecurityGroups = self._filterSecurityGroupsWithProtocolPortOpenFromInternet(allSecurityGroups, 'tcp', 3389)
        self.assertEqual([], rdpOpenSecurityGroups, "Security group(s) with RDP allowed from Internet[vpcId:groupId]: %s. Recommendation: 4.2" % self._groupIdsVpcIds(rdpOpenSecurityGroups))

    def testPortsOpenFromTheInternet(self):
        allSecurityGroups = self._getAllSecurityGroups()
        internetOpenSecurityGroups = self._filterSecurityGroupsWithAccessOpenFromInternet(allSecurityGroups)
        file = open('artifacts/internet_open_security_groups.csv', 'w')
        file.write("VPC ID, Security Group ID")
        for securityGroup in self._groupIdsVpcIds(internetOpenSecurityGroups).split(','):
            file.write('\n'+ securityGroup.replace(':',','))

    def testApiTerminationIsDisabled(self):
        unprotectedInstances = self._instanceWithDisabledTerminantionProtection()
        self.assertEqual([],unprotectedInstances,"Instance(s) with API Terminantion Enabled :%s. Recommended : " % self._instanceIds(unprotectedInstances)) 

    def _getAllSecurityGroups(self):
        securityGroups = []
        for sg in EC2().getSecurityGroups()['SecurityGroups']:
            securityGroup = SecurityGroup(sg['VpcId'], sg['GroupId'], sg['IpPermissions'])
            securityGroups.append(securityGroup)
        return securityGroups

    def _filterSecurityGroupsWithAccessOpenFromInternet(self, securityGroups):
        sgs = []
        for securityGroup in securityGroups:
            if securityGroup.inboundAccessOpenFromInternet():
                sgs.append(securityGroup)
        return sgs

    def _filterSecurityGroupsWithProtocolPortOpenFromInternet(self, securityGroups, protocol, port):
        sgs = []
        for securityGroup in securityGroups:
            if securityGroup.inboundProtocolPortOpenFromInternet(protocol, port):
                sgs.append(securityGroup)
        return sgs

    def _groupIdsVpcIds(self, securityGroups):
        ids = []
        for sg in securityGroups:
            ids.append(sg.vpcId + ":" + sg.groupId)
        return ",".join(ids)

    def _instanceWithDisabledTerminantionProtection(self):
        instances = EC2().getInstances().all()
        return filter(self._disabledTerminationProtection,instances)

    def _disabledTerminationProtection(self,instance):
        apiTerminationAttributes = instance.describe_attribute(Attribute='disableApiTermination')
        return apiTerminationAttributes['DisableApiTermination']['Value'] == False

    def _instanceIds(self,instances):
        return ",".join(map(lambda instance: instance.id, instances))
