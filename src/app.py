# import required modules/packages
from aws_access import ResourceMap, ResourceLoader
import boto3

# initialize aws resource map and loader
res_map = ResourceMap()
res_loader = ResourceLoader(res_map)

# initialize aws boto3 api and get client-providers
ec2 = boto3.client('ec2')

res_loader.load_vpcs(ec2)

print(res_map.res_map)