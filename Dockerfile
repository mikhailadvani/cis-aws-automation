FROM ubuntu

RUN apt update

RUN apt dist-upgrade -y

RUN apt install -y python-pip git

RUN pip install --upgrade pip

RUN pip install boto3 pyyaml

RUN mkdir /opt/aws-security-test

ADD . /opt/aws-security-test 

WORKDIR /opt/aws-security-test

CMD python aws_security_test.py -c config/default.yml; cp test_results.html /output; cp artifacts/* /output
