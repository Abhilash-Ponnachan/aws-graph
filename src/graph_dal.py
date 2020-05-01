# import necessary modules/packages
from neo4j import GraphDatabase
import configparser


# repository class to handle graph db interface
class GraphRepository:
    # read connection details from .secrets config
    def __get_connection_info(self):
        config = configparser.ConfigParser()
        config.read('.secrets')
        uri=config['neo4j']['uri']
        user = config['neo4j']['user']
        password = config['neo4j']['password']
        dbname = config['neo4j']['dbname']
        return (uri, user, password, dbname)
    
    # constructor
    def __init__(self):
        conn_info = self.__get_connection_info()
        self.uri, self.user, self.password, self.dbname = conn_info

    # connect to db
    def connect(self):
        self.__driver = GraphDatabase.driver(self.uri
                                    , auth=(self.user, self.password)
                                    , encrypted=False)
    
    # create node and add properties
    def create_node(self, tranx, label, res_id, props):
        cmd_bfr = []
        # create cmd with lable and id
        cmd_bfr.append("CREATE (n:{0} {{res_id: \"{1}\"".format(label, res_id))
        # add properties
        for p in props:
            kv = ", {0}: \"{1}\" ".format(p[0], p[1])
            cmd_bfr.append(kv)

        # close create cmd
        cmd_bfr.append("})")
        
        # join list items to one one string
        cmd = ''.join(txt for txt in cmd_bfr)
        print(cmd)
        #tranx.run(cmd)
        
    # do db population using callbacks
    def populate_db(self, cb_create_node, cb_create_rels):
        # Note community edition of Neo4j we can only wrok withdefault db
        with self.__driver.session() as session:
            # start transaction
            tranx = session.begin_transaction()
            # clear databse
            session.run("MATCH (n) DETACH DELETE n")
            # callback to create nodes
            cb_create_node(self, tranx)
            # callback to create relationships
            cb_create_rels(self, tranx)
            tranx.commit()

    # close connection
    def close(self):
        self.__driver.close()