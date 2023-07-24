from neo4j import GraphDatabase

# Credenziali d'accesso Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

# Creazione del DB su Neo4j
# Connessione al database Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    print('Connessione stabilita')

    # Creazione di Constraint e Index
    session.run("create constraint for (a:Agency) require a.id is unique;")
    session.run("create constraint for (r:Route) require r.id is unique;")
    session.run("create constraint for (t:Trip) require t.id is unique;")
    session.run("create index for (t:Trip) on (t.service_id);")
    session.run("create constraint for (s:Stop) require s.id is unique;") 
    session.run("create index for (s:Stoptime) on (s.stop_sequence);")
    session.run("create index for (s:Stop) on (s.name);")
    session.run("create constraint for (s:Service) require s.service_id is unique;")
    session.run("create constraint for (d:Day) require d.day is unique;")
    print('Constraint e indici creati...')

    print("Inserimento del'Agenzia")
    query = """load csv with headers from  
            'file:///agency.txt' as csv  
            create (:Agency {name: csv.agency_name, url: csv.agency_url, timezone: csv.agency_timezone});"""
    session.run(query)

    print("Inserimento delle Routes")
    query = """load csv with headers from  
            'file:///routes.txt' as csv  
            match (a:Agency {name: 'aMo Modena'})  
            create (a)-[:OPERATES]->(:Route {id: csv.route_id, short_name: csv.short_name, long_name: csv.route_long_name, type: toInteger(csv.route_type)});"""
    session.run(query)

    print("Inserimento dei Trip")
    query = """load csv with headers from 
            'file:///trips.txt' as csv
            match (r:Route {id: csv.route_id})
            create (r)<-[:USES]-(:Trip {service_id: csv.service_id, id: csv.trip_id, direction_id: csv.direction_id, shape_id: csv.shape_id, headsign: csv.trip_headsign});"""
    session.run(query)

    print("Inserimento degli Stop")
    query = """load csv with headers from 
            'file:///stops.txt' as csv  
            create (:Stop {id: csv.stop_id, name: csv.stop_name, lat: toFloat(csv.stop_lat), lon: toFloat(csv.stop_lon)});"""
    session.run(query)

    print("Inserimento degli StopTimes")
    query = """CALL apoc.periodic.iterate(
            "load csv with headers from 'file:///stop_times.txt' as csv return csv",
            "match (t:Trip {id: csv.trip_id}), (s:Stop {id: csv.stop_id}) create (t)<-[:PART_OF_TRIP]-(st:Stoptime {arrival_time: csv.arrival_time, departure_time: csv.departure_time, stop_sequence: toInteger(csv.stop_sequence)})-[:LOCATED_AT]->(s)",
            {batchSize:1000, parallel:true})"""
    session.run(query)

    print("Inserimento delle relazioni tra gli StopTimes")
    query = """match (s1:Stoptime)-[:PART_OF_TRIP]->(t:Trip),  
            (s2:Stoptime)-[:PART_OF_TRIP]->(t)  
            where s2.stop_sequence=s1.stop_sequence+1  
            create (s1)-[:PRECEDES]->(s2);"""
    session.run(query)

    print("Assicurarsi di aver caricato il file new_calendar_dates.txt realizzato con lo script reshape.py")
    print("Inserimento dei services")
    query = """load csv with headers from 'file:///new_calendar_dates.txt' as csv
            merge (:Service {service_id: csv.service_id})"""
    session.run(query)

    print("Collegamento services con i trip")
    query = """MATCH (s:Service), (t:Trip) where t.service_id = s.service_id merge (t)-[:SERVICE_TYPE]->(s)"""
    session.run(query)

    print("Inserimento dei giorni in cui sono disponibili i servizi")
    query = """CALL apoc.periodic.iterate(
            "load csv with headers from 'file:///new_calendar_dates.txt' as csv return csv",
            "match (s:Service {service_id: csv.service_id}) merge (d:Day {day:date(csv.day)}) merge (s)-[:VALID_IN]->(d) SET d.exception_type = csv.exception_type",
            {batchSize:500})"""
    session.run(query)

    print("Inserimento delle relazioni tra gli Stop vicini")
    query = """MATCH (s1:Stop)
            WITH point({x: s1.lat, y: s1.lon, crs: 'cartesian'}) AS p1, s1
            MATCH (s2:Stop)
            WITH point({x: s2.lat, y: s2.lon, crs: 'cartesian'}) AS p2, p1, s1, s2
            WHERE s1.id <> s2.id AND point.distance(p1,p2) < 0.0009
            MERGE (s1)-[:WALK_TO]->(s2);"""
    session.run(query)

    print('DB realizzato correttamente')