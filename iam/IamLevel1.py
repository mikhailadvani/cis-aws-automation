import unittest
from aws.api import IAM
from aws.entity import IAMUser

class IamLevel1(unittest.TestCase):
    def testMfaEnabledForConsoleUsers(self):
        iamUsersWithoutMfa = []
        for iamUser in self._getIamUserList():
            if not iamUser.mfaEnabled():
                iamUsersWithoutMfa.append(iamUser)
        self.assertEqual([], iamUsersWithoutMfa, "Users %s have console passwords without MFA" % self._users(iamUsersWithoutMfa))

    def testUnusedCredentialsAreDeactivated(self):
        oldUserTimePeriod = 90
        iamUsersWithUnusedCredentials = []
        for iamUser in self._getIamUserList():
            if ((not iamUser.credentialsUsed(oldUserTimePeriod)) | (not iamUser.accessKeysUsed(oldUserTimePeriod))):
                iamUsersWithUnusedCredentials.append(iamUser)
        self.assertEqual([], iamUsersWithUnusedCredentials, "Active users %s have passwords/access keys unused for long" % self._users(iamUsersWithUnusedCredentials))

    def testAccessKeysAreRotated(self):
        oldAccessKeyTimePeriodInDays = 90
        iamUsersWithOldAccessKeys = []
        for iamUser in self._getIamUserList():
            if not iamUser.accessKeysRotated(oldAccessKeyTimePeriodInDays):
                iamUsersWithOldAccessKeys.append(iamUser)
        self.assertEqual([], iamUsersWithOldAccessKeys, "Active users %s have access keys not rotated for long" % self._users(iamUsersWithOldAccessKeys))

    def testPasswordPolicyRequiresUpperCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireUppercaseCharacters'), "Password policy does not mandate upper case characters in password")

    def testPasswordPolicyRequiresLowerCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireLowercaseCharacters'), "Password policy does not mandate lower case characters in password")

    def testPasswordPolicyRequiresNumbers(self):
        self.assertTrue(self._getPasswordPolicyField('RequireNumbers'), "Password policy does not mandate numbers in password")

    def testPasswordPolicyRequiresSymbols(self):
        self.assertTrue(self._getPasswordPolicyField('RequireSymbols'), "Password policy does not mandate symbols in password")

    def testPasswordPolicyRequiresMinimumLength(self):
        requirePasswordLength = 14
        self.assertTrue(self._getPasswordPolicyField('MinimumPasswordLength') >= requirePasswordLength, "Password policy does not mandate required minimum length of password")

    def _getPasswordPolicyField(self, field):
        passwordPolicy = IAM().getPasswordPolicy()
        return passwordPolicy['PasswordPolicy'][field]

    def _getIamUserList(self):
        iamUserList = []
        users = IAM().getCredentialReport()
        for user in users:
            iamUser = IAMUser(user)
            iamUserList.append(iamUser)
        return iamUserList

    def _users(self, iamUsers):
        users = []
        for iam in iamUsers:
            users.append(iam.user)
        return ",".join(users)