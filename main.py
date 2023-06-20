import peartree as pt
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "Public Transport"
password = "password"

# Connessione al database Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    print('Connected')