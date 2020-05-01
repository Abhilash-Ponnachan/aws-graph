from neo4j import GraphDatabase
from graph_dal import GraphRepository

def get_movie(trnx, name):
	for rec in trnx.run("MATCH (a:Person)-[r]->(m:Movie) "
						 "WHERE m.title = $name "
                         "RETURN a,r", name=name):
		print(rec)

def create_nodes(repo, tranx):
	label = "VPC"
	res_id = "vpc-03cfe3989f888508a"
	props = [('name', 'Rand-VPC'), 
			('cidr_block', '10.0.0.0/16'), 
			('is_default', False)]
	repo.create_node(tranx, label, res_id, props)
    
def create_rels(repo, tranx):
	print('create rels with - {}'.format(tranx))


# connect to graph db
graph_repo = GraphRepository()
graph_repo.connect()
try:
	graph_repo.populate_db(create_nodes, create_rels)
finally:
	graph_repo.close()