response = {
    "took": 4,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {"value": 2, "relation": "eq"},
        "max_score": 1.0703217,
        "hits": [
            {
                "_index": "my_index",
                "_id": "3",
                "_score": 1.0703217,
                "_source": {
                    "title": "Document 3",
                    "type": "text",
                    "content": "Cars have controls i am for driving, parking, passenger comfort, and a variety of lamps."
                },
                "highlight": {
                    "content": ["Cars have controls <p class='main'>i am</p> for driving, parking, passenger comfort, and a variety of lamps."]
                }
            },
            {
                "_index": "my_index",
                "_id": "1",
                "_score": 0.8438319,
                "_ignored": ["content.keyword"],
                "_source": {
                    "title": "car.txt",
                    "type": "text",
                    "content": "TAnimals i am happy are multicellular, eukaryotic organisms in the biological kingdom Animalia."
                },
                "highlight": {
                    "content": ["TAnimals <p class='main'>i am</p> happy are multicellular, eukaryotic organisms in the biological kingdom Animalia."]
                }
            }
        ]
    }
}

formatted_response = f'''
Took: {response['took']}
Timed out: {response['timed_out']}
Total shards: {response['_shards']['total']}
Successful shards: {response['_shards']['successful']}
Skipped shards: {response['_shards']['skipped']}
Failed shards: {response['_shards']['failed']}

Hits total: {response['hits']['total']['value']}
Max score: {response['hits']['max_score']}

Hits:
'''
for hit in response['hits']['hits']:
    formatted_response += f'''
Index: {hit['_index']}
ID: {hit['_id']}
Score: {hit['_score']}
Source: {hit['_source']}
Highlight: {hit['highlight']}
'''

print(formatted_response)
