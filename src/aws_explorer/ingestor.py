import cPickle as pickle
import json
import os
import os.path
import time
import uuid

import boto
from py2neo import neo4j, rel, node

USE_CACHE = True


#class ASGHandler(object):

    #def __init__(self,


#resource_handler_map = {
    #AWS::AutoScaling::AutoScalingGroup
    #AWS::AutoScaling::LaunchConfiguration
    #AWS::AutoScaling::ScalingPolicy
    #AWS::AutoScaling::Trigger
    #AWS::CloudFormation::Authentication
    #AWS::CloudFormation::CustomResource
    #AWS::CloudFormation::Init
    #AWS::CloudFormation::Stack
    #AWS::CloudFormation::WaitCondition
    #AWS::CloudFormation::WaitConditionHandle
    #AWS::CloudFront::Distribution
    #AWS::CloudWatch::Alarm
    #AWS::DynamoDB::Table
    #AWS::EC2::CustomerGateway
    #AWS::EC2::DHCPOptions
    #AWS::EC2::EIP
    #AWS::EC2::EIPAssociation
    #AWS::EC2::Instance
    #AWS::EC2::InternetGateway
    #AWS::EC2::NetworkAcl
    #AWS::EC2::NetworkAclEntry
    #AWS::EC2::NetworkInterface
    #AWS::EC2::NetworkInterfaceAttachment
    #AWS::EC2::Route
    #AWS::EC2::RouteTable
    #AWS::EC2::SecurityGroup
    #AWS::EC2::SecurityGroupIngress
    #AWS::EC2::SecurityGroupEgress
    #AWS::EC2::Subnet
    #AWS::EC2::SubnetNetworkAclAssociation
    #AWS::EC2::SubnetRouteTableAssociation
    #AWS::EC2::Volume
    #AWS::EC2::VolumeAttachment
    #AWS::EC2::VPC
    #AWS::EC2::VPCDHCPOptionsAssociation
    #AWS::EC2::VPCGatewayAttachment
    #AWS::EC2::VPNConnection
    #AWS::EC2::VPNConnectionRoute
    #AWS::EC2::VPNGateway
    #AWS::ElastiCache::CacheCluster
    #AWS::ElastiCache::ParameterGroup
    #AWS::ElastiCache::SecurityGroup
    #AWS::ElastiCache::SecurityGroupIngress
    #AWS::ElastiCache::SubnetGroup
    #AWS::ElasticBeanstalk::Application
    #AWS::ElasticBeanstalk::Environment
    #AWS::ElasticLoadBalancing::LoadBalancer
    #AWS::IAM::AccessKey
    #AWS::IAM::Group
    #AWS::IAM::InstanceProfile
    #AWS::IAM::Policy
    #AWS::IAM::Role
    #AWS::IAM::User
    #AWS::IAM::UserToGroupAddition
    #AWS::RDS::DBInstance
    #AWS::RDS::DBParameterGroup
    #AWS::RDS::DBSubnetGroup
    #AWS::RDS::DBSecurityGroup
    #AWS::RDS::DBSecurityGroupIngress
    #AWS::Route53::RecordSet
    #AWS::Route53::RecordSetGroup
    #AWS::S3::Bucket
    #AWS::S3::BucketPolicy
    #AWS::SDB::Domain
    #AWS::SNS::TopicPolicy
    #AWS::SNS::Topic
    #AWS::SQS::Queue
    #AWS::SQS::QueuePolicy


def load_autoscaling_group(group_name, asg, graph_db):
    group = asg.get_all_groups([group_id])
    properties = {
        'name': group.name,
        'default_cooldown': group.default_cooldown,
        'desired_capacity': group.desired_capacity,
        'health_check_period': group.health_check_period,
        'health_check_type': health_check_type,
        'max_size': max_size,
        'min_size': min_size,
        'placement_group': placement_group,
        'vpc_zone_identifier': vpc_zone_identifier,
    }
    graph_db.get_or_create_indexed_node(
        'auto_scaling_group',
        'name',
        group.name,
        node(group)
    )


def load_cfn_stacks(cfn, graph_db):
    stacks = []
    if not os.path.exists('./cache/stacks'):
        os.mkdir('cache/stacks')
    if USE_CACHE:
        stack_list = []
        for path in os.listdir('./cache/stacks'):
            with open("./cache/stacks/{0}".format(path)) as handle:
                stack_list.append(pickle.loads(handle.read()))
    else:
        stack_list = cfn.list_stacks()

    for stack in stack_list:
        stack.stack_name, stack.template_description
        template = cfn.get_template(
            stack.stack_id
        )['GetTemplateResponse']['GetTemplateResult']['TemplateBody']
        properties = dict(
            name=stack.stack_name,
            stack_id=stack.stack_id,
            description=stack.template_description,
            template=template,
            stack_status=stack.stack_status,
            creation_time=stack.creation_time
        )
        file_path = "./cache/stacks/{0}.ser".format(uuid.uuid4().hex)
        with open(file_path, 'w') as handle:
            handle.write(pickle.dumps(stack))
        stacks.append(properties)
        time.sleep(2)

    batch = neo4j.WriteBatch(graph_db)
    for stack in stacks:
        batch.get_or_create_indexed_node(
            'cfn_stacks',
            'stack_id',
            stack['stack_id'],
            node(stack)
        )
    nodes = batch.submit()


def get_all_stacks():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")


if __name__ == '__main__':
    cfn = boto.connect_cloudformation()
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

    load_cfn_stacks(cfn, graph_db)
