from neo4j import GraphDatabase

def get_credentials():
	return ("neo4j", "Sample")

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