from neo4j import GraphDatabase
from datetime import datetime

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

# Coordinate del dipartimento di ingegneria di Modena
lat = 44.6293839463985
lon = 10.948827844203144
# Coordinate Largo Garibaldi Modena
lat = 44.64374610736016
lon = 10.93231058316037

# Nome della fermata di arrivo FINZI, D'AVIA, POLO LEONARDO, GALILEI
dest = "FINZI"

# Connessione al database Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    print('Connected')

    # Prendi il nodo più vicino alle coordinate date
    query = """MATCH (s:Stop)
            WITH point({x: $lat, y: $lon, crs: 'cartesian'}) AS p1, point({x: s.lat, y: s.lon, crs: 'cartesian'}) AS p2, s
            RETURN s, point.distance(p1,p2) AS dist ORDER BY dist ASC LIMIT 1"""
    result = session.run(query, lat=lat, lon=lon)
 
    for record in result:
        lat,lon,name = record["s"].get('lat'), record["s"].get('lon'), record["s"].get('name')

    # Ottieni l'orario attuale
    now = datetime.now()
    formatted_time = now.strftime('%H:%M:%S')
    paths = None

    # Calcola il percorso per raggiungere la fermata desiderata
    query = """MATCH (s:Stop {name:$name}), (f:Stop {name:$dest})
            MATCH p=(s)-[:LOCATED_AT]-(s1:Stoptime)-[:PART_OF_TRIP]-(:Trip)-[:PART_OF_TRIP]-(s2:Stoptime)-[:LOCATED_AT]-(f) 
            WHERE $formatted_time <= s1.departure_time < s2.arrival_time 
            RETURN p ORDER BY s1.departure_time ASC LIMIT 1"""
    result = session.run(query, name=name, formatted_time=formatted_time, dest=dest)

    for record in result:
        paths = record["p"]

    # Prova con una fermata intermedia
    if paths == None:
        query2 = """MATCH (s:Stop {name:$name}), (f:Stop {name:$dest})
                MATCH p=(s)-[:LOCATED_AT]-(s1:Stoptime)-[:PART_OF_TRIP]-(:Trip)-[:PART_OF_TRIP]-(s2:Stoptime)-[:LOCATED_AT]-(:Stop)-[:LOCATED_AT]-(s3:Stoptime)-[:PART_OF_TRIP]-(:Trip)-[:PART_OF_TRIP]-(s4:Stoptime)-[:LOCATED_AT]-(f)
                WHERE $formatted_time <= s1.departure_time < s2.arrival_time < s3.departure_time < s4.arrival_time 
                RETURN p ORDER BY s1.departure_time ASC, s3.departure_time ASC LIMIT 1
            """
        result = session.run(query2, name=name, formatted_time=formatted_time, dest=dest)
    for record in result:
        paths = record["p"]

    # Iterazione attraverso i nodi e le relazioni all'interno del percorso
    i = 'Partenza'
    for node in paths.nodes:
        if node["name"] != None:
            print(f"Fermata di {i}:", node["name"])
            i = 'Partenza'
        elif node["short_name"] != None:
            print("Tratta Autobus:", node["short_name"])
        elif node["departure_time"] != None:
            print(f"Orario di {i}:", node["departure_time"])
            i = 'Arrivo'