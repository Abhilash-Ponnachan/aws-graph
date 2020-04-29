from neo4j import GraphDatabase
import configparser

def get_credentials():
	# read credetials from .secrets INI file
	config = configparser.ConfigParser()
	config.read('.secrets')
	user = config['neo4j']['user']
	password = config['neo4j']['password']
	return (user, password)

def get_movie(trnx, name):
	for rec in trnx.run("MATCH (a:Person)-[r]->(m:Movie) "
						 "WHERE m.title = $name "
                         "RETURN a,r", name=name):
		print(rec)


URI = "bolt://localhost:7687"

driver = GraphDatabase.driver(URI, auth=get_credentials(), encrypted=False)
try:
	with driver.session() as session:
		session.read_transaction(get_movie, 'The Matrix')

finally:
	driver.close()