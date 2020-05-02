# import required modules/packages
from aws_access import ResourceMap, ResourceLoader
from graph_dal import GraphRepository
import boto3
from utils import *

if __name__ == "__main__":
    # initialize aws resource map and loader
    res_map = ResourceMap()
    res_loader = ResourceLoader(res_map)

    # initialize aws boto3 api and get client-providers
    ec2 = boto3.client('ec2')

    # load AWS resources
    res_loader.load_vpcs(ec2).load_Subnets(ec2) \
        .load_Igws(ec2).load_sec_grps(ec2)

    # callback handler to add nodes
    @entry_deco("++++++ Creating Nodes ... ++++++")
    def create_nodes(repo, tranx):
        for res_type, res_items in res_map.res_items():
            if not res_items:
                continue
            for res_id, res_data in res_items.items():
                _, _, *props = res_data._asdict().items()
                repo.create_node(tranx, res_type.name, res_id, props)
                
    # callback handler to add relationships
    @entry_deco("++++++ Creating Relationships ... ++++++")
    def create_rels(repo, tranx):
        pass

    # connect to graph db
    graph_repo = GraphRepository()
    graph_repo.connect()
    try:
        graph_repo.populate_db(create_nodes, create_rels)
    finally:
        graph_repo.close()

