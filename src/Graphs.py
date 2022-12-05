import rdflib
from rdflib import URIRef

class Graphs:
    def __init__(self):
        self.load_graphs()
    
    def load_graphs(self):
        self.graph = rdflib.Graph()
        print("Please wait while graph is loading ...")
        self.graph.parse('data/14_graph.nt', format="turtle")
        print("Graph loaded")
    
    def get_graph(self):
        return self.graph
    
    def queryMultimedia(self, p):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        SELECT ?item WHERE {
            wd:%s wdt:P18 ?item .
        }''' % (p)
        responses = self.graph.query(query)
        res_list = [str(result.item) for result in responses]
        return res_list
    
    def queryMultimedia2(self, p):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        SELECT ?item WHERE {
            wd:%s wdt:P345 ?item .
        }''' % (p)
        responses = self.graph.query(query)
        res_list = [str(result.item) for result in responses]
        return res_list
    
    def queryFactual(self, id, p):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        SELECT ?item WHERE {
            wd:%s wdt:%s ?element .
            ?element rdfs:label ?item
        }''' % (id, p)
        responses = self.graph.query(query)
        res_list = [str(result.item) for result in responses]
        return res_list

    def QueryMoviesfromDirector(self, id):
        query = '''
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX bd: <http://www.bigdata.com/rdf#>

        SELECT DISTINCT ?itemLabel WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            {
                SELECT DISTINCT ?item WHERE {
                    ?item p:P57 ?statement0.
                    ?statement0 (ps:P57/(wdt:P279*)) ?director.
                    wd:%s wdt:P57 ?director .
                }
                LIMIT 10
            }
        }''' % id
        responses = self.graph.query(query)
        movie_names = [str(result.itemLabel) for result in responses]
        # res_list_2 = [str(result.item) for result in responses]
        print(movie_names)
        return movie_names
               

if __name__=="__main__":
    g = Graphs()
    g.queryMultimedia("Q1033016")
    g.queryFactual("Q223596", "P162")