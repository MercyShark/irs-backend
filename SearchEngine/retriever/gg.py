from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')


# es.indices.delete(index="my_document_index")
es.delete(index="gg_index",id="G4sSvo4BVAntUERQTtgM")