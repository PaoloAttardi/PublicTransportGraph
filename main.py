from matplotlib import pyplot as plt
import peartree as pt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from neo4j import GraphDatabase

gtfs_file_path = "GTFS_230406_240405.zip"
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

# Carica il feed GTFS utilizzando peartree
feed = pt.get_representative_feed(gtfs_file_path)
trips = feed.trips
tmp = trips[trips['trip_id'] == '1022_10']
print(tmp)

'''routes = feed.routes
trips = feed.trips
stops = feed.stops
stop_times = feed.stop_times
agency = feed.agency'''

# Genera il grafo
start = 6*60*60 + 58*60  # 6:58 AM
end = 7*60*60  # 7:00 AM
graph = pt.load_feed_as_graph(feed,start,end) # graph è un multigrafo --> si può aggiungere lo stesso edge più volte

# pt.generate_plot(graph)
# write_dot(graph, 'graph.dot')
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
edge_labels=dict([((u,v,),d['length'])
             for u,v,d in graph.edges(data=True)])

# plt.show()
plt.savefig('graph.png')

# Visualizza il contenuto dei nodi del grafo
for node in graph.nodes(data=True):
    id,data = node
    print(id,data)
    break

for edge in graph.edges(data=True):
    node1,node2,data = edge
    print(f'Edge che collega {node1} a {node2} con i seguenti dati {data}')
    print(data['mode'])
    break

# Connessione al database Neo4j
# driver = GraphDatabase.driver(uri, auth=(username, password))

# with driver.session() as session:
#    print('Connected')