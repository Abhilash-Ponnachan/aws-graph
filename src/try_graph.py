from neo4j import GraphDatabase
import configparser

def get_connection_info():
	# read credetials from .secrets INI file
	config = configparser.ConfigParser()
	config.read('.secrets')
	uri=config['neo4j']['uri']
	user = config['neo4j']['user']
	password = config['neo4j']['password']
	dbname = config['neo4j']['dbname']
	return (uri, user, password, dbname)

def get_movie(trnx, name):
	for rec in trnx.run("MATCH (a:Person)-[r]->(m:Movie) "
						 "WHERE m.title = $name "
                         "RETURN a,r", name=name):
		print(rec)

uri, user, password, dbname = get_connection_info()

driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
try:
	with driver.session() as session:
		session.read_transaction(get_movie, 'The Matrix')

finally:
	driver.close()