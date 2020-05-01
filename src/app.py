# import required modules/packages
from aws_access import ResourceMap, ResourceLoader
from graph_dal import GraphRepository
import boto3

if __name__ == "__main__":
    # initialize aws resource map and loader
    res_map = ResourceMap()
    res_loader = ResourceLoader(res_map)

    # initialize aws boto3 api and get client-providers
    ec2 = boto3.client('ec2')

    # load AWS resources
    res_loader.load_vpcs(ec2)

    print(res_map.res_map)

    def create_nodes(session):
        print('create nodes with - {}'.format(session))
    
    def create_rels(session):
        print('create rels with - {}'.format(session))


    # connect to graph db
    graph_repo = GraphRepository()
    graph_repo.connect()
    try:
        graph_repo.populate_db(create_nodes, create_rels)
    finally:
        graph_repo.close()

