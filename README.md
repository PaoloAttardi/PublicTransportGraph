# PublicTransportGraph
Rappresentazione del Trasporto pubblico Modenese in un Database a grafo partendo dal rispettivo file GTFS 

## Creazione del Db
La creazione del Db avviene tramite l'esecuzione del file dbSetup.py che esegue le seguenti operazioni:

1. Esegue la connessione ad un'istanza di Db su Neo4j
2. Crea i Constraint e gli indici utili per la realizzazione della struttura a grafo
3. Aggiunge i nodi e crea le relazioni tra questi partendo dai file ricavati dal feed GTFS

### Prerequisiti
