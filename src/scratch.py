props = [
    ('name', 'default'), ('desc', 'default VPC security group'), ('vpc_id', 'vpc-661ce91f'), 
    ('ingress_perms', 
        [
         {'IpRanges': [], 
         'UserIdGroupPairs': 
            [
                {'UserId': '164573711423', 
                'GroupId': 'sg-b06c79ff'
                }
            ], 
            'Ipv6Ranges': [], 
            'IpProtocol': '-1', 
            'PrefixListIds': []
            }
        ]
    ), 
    ('egress_perms', 
        [
            {'IpRanges': 
                [
                    {'CidrIp': '0.0.0.0/0'}
                ], 
                'UserIdGroupPairs': [], 
                'Ipv6Ranges': [], 
                'IpProtocol': '-1', 
                'PrefixListIds': []
            }
        ]
    )
]

def iter_props(props, cb_handler):
    # helper func to handle list items
    def iter_list(items):
        for itm in items:
            if isinstance(itm, list):
                iter_list(itm)
            elif isinstance(itm, dict):
                iter_dict(itm)
    # helper func to handle dict items
    def iter_dict(items):
        for key, val in items.items():
            if isinstance(val, list):
                iter_list(val)
            elif isinstance(val, dict):
                iter_dict(val)
            else:
                cb_handler(key, val)
    # outer func to go over properties
    for prop in props:
        key, value = prop
        if isinstance(value, dict):
            iter_dict(value)
        elif isinstance(value, list):
            iter_list(value)            
        else:            
            cb_handler(key, value)

iter_props(props, lambda k, v : print("{} -> {}".format(k, v)))