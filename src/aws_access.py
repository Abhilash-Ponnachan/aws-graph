# import necessary modules/packages
import enum
from collections import namedtuple
from utils import *

# enum for resource types
class ResType(enum.Enum):
    VPCS = 1
    SUB_NETS = 2
    IGWS = 3
    SEC_GRPS = 4
    ROUTE_TBLS = 5


# types to represent each resource type
VPC = namedtuple('VPC', 'res_type id name cidr_block is_default')
SUB_NET = namedtuple('SUB_NET', 'res_type id name az_id vpc_id state az_default cidr_block')
IGWS = namedtuple('IGWS', 'res_type id name vpc_id state')
SEC_GRPS = namedtuple('SEC_GRPS', 'res_type id name desc vpc_id ingress_perms egress_perms')
IGWS = namedtuple('IGWS', 'res_type id name vpc_id state')
ROUTE_TBLS = namedtuple('ROUTE_TBLS', 'res_type id name vpc_id associations routes')

# collection class that holds all our AWS resources
class ResourceMap:
    def __init__(self):
        self.res_map = {
            ResType.VPCS:{},
            ResType.SUB_NETS:{},
            ResType.IGWS:{},
            ResType.SEC_GRPS:{},
            ResType.ROUTE_TBLS:{}
        }
    
    def clear(self):
        for res in self.res_map.values():
            res.clear()

    def add_item(self, res_type: ResType, id, res):
        res_typ_map = self.res_map[res_type]
        res_typ_map[id] = res

    def res_items(self):
        return self.res_map.items()

# adapter class to load AWS resources
class ResourceLoader:
    def __init__(self, res_map: ResourceMap):
        self.res_map = res_map
    
    def extract_name(tags):
        for k_v in tags:
            k = k_v.get('Key')
            if k == 'Name':
                v = k_v.get('Value')
                return v
        return None
    extract_name = staticmethod(extract_name)

    @entry_deco("++++++ loading VPCS ... ++++++")
    def load_vpcs(self, ec2):
        vpcs = ec2.describe_vpcs()
        for v in vpcs['Vpcs']:
            id = v['VpcId']
            self.res_map.add_item(
                        ResType.VPCS, 
                        id, 
                        VPC(
                            res_type=ResType.VPCS,
                            id = id,
                            name = ResourceLoader.extract_name(v['Tags']),
                            cidr_block=v['CidrBlock'],
                            is_default=v['IsDefault']
                            )
                        )
        # return self for 'fluent api'
        return self

    @entry_deco("++++++ loading Subents ... ++++++")
    def load_Subnets(self, ec2):
        sbnts = ec2.describe_subnets()
        for sn in sbnts['Subnets']:
            id = sn['SubnetId']
            self.res_map.add_item(
                        ResType.SUB_NETS, 
                        id, 
                        SUB_NET(
                            res_type=ResType.SUB_NETS,
                            id=id,
                            name=ResourceLoader.extract_name(sn['Tags']),
                            az_id=sn['AvailabilityZoneId'],
                            vpc_id=sn['VpcId'],
                            state=sn['State'],
                            az_default=sn['DefaultForAz'],
                            cidr_block=sn['CidrBlock']
                            )
                        )
        # return self for 'fluent api'
        return self

    @entry_deco("++++++ loading IGWs ... ++++++")
    def load_Igws(self, ec2):
        igws = ec2.describe_internet_gateways()
        for igw in igws['InternetGateways']:
            id = igw['InternetGatewayId']
            atchmts = igw['Attachments']
            vpc_id, state = '', ''
            if atchmts:
                state = atchmts[0]['State']
                vpc_id = atchmts[0]['VpcId']
            self.res_map.add_item(
                        ResType.IGWS, 
                        id, 
                        IGWS(
                            res_type=ResType.SUB_NETS,
                            id=id,
                            name=ResourceLoader.extract_name(igw['Tags']),
                            vpc_id=vpc_id,
                            state=state,
                            )
                        )
        # return self for 'fluent api'
        return self
    
    @entry_deco("++++++ loading Security Groups ... ++++++")
    def load_sec_grps(self, ec2):
        sec_grps = ec2.describe_security_groups()
        for sg in sec_grps['SecurityGroups']:
            id = sg['GroupId']
            in_perms = sg['IpPermissions']
            out_perms = sg['IpPermissionsEgress']
            self.res_map.add_item(
                        ResType.SEC_GRPS, 
                        id, 
                        SEC_GRPS(
                            res_type=ResType.SEC_GRPS,
                            id=id,
                            name=sg['GroupName'],
                            desc=sg['Description'],
                            vpc_id=sg['VpcId'],
                            ingress_perms=in_perms,
                            egress_perms=out_perms
                            )
                        )
        # return self for 'fluent api'
        return self

    @entry_deco("++++++ loading Route Tables ... ++++++")
    def load_rt_tbls(self, ec2):
        rt_tbls = ec2.describe_route_tables()
        for rt in rt_tbls['RouteTables']:
            id = rt['RouteTableId']
            associations = rt['Associations']
            routes = rt['Routes']
            self.res_map.add_item(
                        ResType.ROUTE_TBLS, 
                        id, 
                        ROUTE_TBLS(
                            res_type=ResType.ROUTE_TBLS,
                            id=id,
                            name=ResourceLoader.extract_name(rt['Tags']),
                            vpc_id=rt['VpcId'],
                            associations=associations,
                            routes=routes
                            )
                        )
        # return self for 'fluent api'
        return self