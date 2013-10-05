"""
This is the entry point for querying an AWS account for resources and
indexing them in ElasticSearch.

Usage:
    crawler <es_host> <es_port>
"""

import requests
import boto
import json

from docopt import docopt

def crawl(config):
    """
    "Crawl" ec2 instances and dump them into elastic search
    """
    ec2 = boto.connect_ec2()
    reservations = ec2.get_all_instances()
    for reservation in reservations:
        for instance in reservation.instances:
            url = "{0}/ec2/instance/{1}".format(config['es_endpoint'],
                    instance.id)
            headers = {'content-type': 'application/json'}
            requests.put(url, headers=headers,
                    data=json.dumps(instance_to_dict(instance)))


def instance_to_dict(instance):
    """
    Convert an instance object to a json serializable dictionary.

    TODO there is probably a better way to do this ...
    """
    return {
        'id': instance.id,
        'public_dns_name': instance.public_dns_name,
        'private_dns_name': instance.private_dns_name,
        'state': instance.state,
        'state_code': instance.state_code,
        'previous_state': instance.previous_state,
        'previous_state_code': instance.previous_state_code,
        'key_name': instance.key_name,
        'instance_type': instance.instance_type,
        'launch_time': instance.launch_time,
        'image_id': instance.image_id,
        'placement': instance.placement,
        'placement_group': instance.placement_group,
        'placement_tenancy': instance.placement_tenancy,
        'kernel': instance.kernel,
        'ramdisk': instance.ramdisk,
        'architecture': instance.architecture,
        'hypervisor': instance.hypervisor,
        'virtualization_type': instance.virtualization_type,
        'product_codes': instance.product_codes,
        'ami_launch_index': instance.ami_launch_index,
        'monitored': instance.monitored,
        'monitoring_state': instance.monitoring_state,
        'spot_instance_request_id': instance.spot_instance_request_id,
        'subnet_id': instance.subnet_id,
        'vpc_id': instance.vpc_id,
        'private_ip_address': instance.private_ip_address,
        'ip_address': instance.ip_address,
        'platform': instance.platform,
        'root_device_name': instance.root_device_name,
        'root_device_type': instance.root_device_type,
        #'block_device_mapping': instance.block_device_mapping,
        'state_reason': instance.state_reason,
        #'groups': instance.groups,
        #'interfaces': instance.interfaces,
        'ebs_optimized': instance.ebs_optimized,
        'instance_profile': instance.instance_profile
    }

if __name__ == "__main__":
    args = docopt(__doc__)
    config = {
        "es_endpoint": "http://{0}:{1}".format(args['<es_host>'],
            args['<es_port>'])
    }
    crawl(config)
