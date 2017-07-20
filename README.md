# Runtime
#### Requirements
- **Python**: 2.7.12
- **Boto3**: 1.4.1

#### Configuring Tests

##### Credentials

Credentials need to be setup as described in [Boto3 Documentation](http://boto3.readthedocs.io/en/latest/guide/configuration.html).
Access needed by the users' API keys configured:

- AmazonEC2ReadOnlyAccess
- IAMReadOnlyAccess
- AWSCloudTrailReadOnlyAccess
- AmazonS3ReadOnlyAccess
- CloudWatchLogsReadOnlyAccess
- CloudWatchReadOnlyAccess
- AmazonSNSReadOnlyAccess
- *KMSReadOnlyPolicy* - There is no pre-defined AWS Policy with the necessary privileges. The custom policy can defined as mentioned in the [documentation](https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies.html#iam-policy-example-read-only-console)

##### Tests to run

Setup a config file similar to [default.yml](https://github.com/mikhailadvani/aws-security-test/blob/master/config/default.yml) to execute desired tests. Value for each test should be `True` or `False`.

#### Execution Steps

##### Run as script
`python aws_security_test.py -c config/default.yml` - Will use the credentials from the environment variables if found or will fall back to the default profile in `~/.aws/config`

`python aws_security_test.py -c config/default.yml -p profile_name` - Will use the credentials from the corresponding profile defined in `~/.aws/config`

#### Run in a docker container

You can run the `aws-security-test` in **docker** and it can be integrated in CI easily:

First, you have to build the image first:

`docker build -t aws-security-test .`

Then you can get the test result via `docker run`:

`docker run -ti -e AWS_DEFAULT_REGION=<AWS_REGION> -e AWS_ACCESS_KEY_ID=<your access key> -e AWS_SECRET_ACCESS_KEY=<your access key_id> -v $(pwd)/artifacts:/output aws-security-test`

Or you can give the environment variables by `--env-file`:

`docker run -ti --env-file <env file> -v $(pwd)/artifacts:/output aws-security-test`

Then the result will output to the `output` directory under your current directory.

You can also give the config file by `-v` or `--volume`:

`docker run -ti --env-file <env file> -v $(pwd)/artifacts:/output -v <your-config-file.yml>:/opt/aws-security-test/config/default.yml aws-security-test`



#### Artifacts

Certain artifacts will be created at the end of every execution for additional verification. The will be in the artifacts directory

`root_login.txt` : Will be useful in monitoring root account access in case CloudWatch is not used.

`sns_subscribers.csv` : Lists subscribers for each SNS topic. Can be used to ensure notifications are being sent to the right audience.

`internet_open_security_groups.csv` : Lists security groups with access open to the Internet. This list might contain rules where access open from the Internet is desired, but can also be used to check for misconfigurations.

# License
Apache License 2.0
