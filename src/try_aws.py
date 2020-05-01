import enum
from collections import namedtuple
from utils import *

# enum for resource types
class ResType(enum.Enum):
    VPCS = 1
    SUB_NETS = 2
    IGWS = 3
    SEC_GRPS = 4


# types to represent each resource type
VPC = namedtuple('VPC', 'res_type id name cidr_block is_default')

# collection class that holds all our AWS resources
class ResourceMap:
    def __init__(self):
        self.res_map = {
            ResType.VPCS:{},
            ResType.SUB_NETS:{},
            ResType.IGWS:{},
            ResType.SEC_GRPS:{}
        }
    
    def clear(self):
        for res in self.res_map.values():
            res.clear()

    def add_item(self, res_type: ResType, id, res):
        res_typ_map = self.res_map[res_type]
        res_typ_map[id] = res


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

    @entry_deco("+++ loading VPCs +++")
    def load_vpcs(self, ec2):
        vpcs = {'Vpcs': [
            {
                'Tags': [{'Value': 'Rand-VPC', 'Key': 'Name'}], 
                'IsDefault': False, 
                'VpcId': 'vpc-03cfe3989f888508a', 
                'CidrBlock': '10.0.0.0/16', 
            },
            {
               'Tags': [{'Value': 'Default-VPC', 'Key': 'Name'}], 
               'IsDefault': True, 
               'VpcId': 'vpc-661ce91f', 
               'CidrBlock': '172.31.0.0/16'
            }
            ]
        }
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
        # return self for 'fluent api' style
        return self


res_map = ResourceMap()

res_loader = ResourceLoader(res_map)
res_loader.load_vpcs(None)
for res in res_map.res_map[ResType.VPCS].values():
    res_typ = res.res_type
    res_id = res.id
    _, _, *props = res._asdict().items()
    print(res_typ, res_id, props)

