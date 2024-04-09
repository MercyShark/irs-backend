{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.8093529,
    "hits": [
      {
        "_index": "my_document_index",
        "_id": "G4sSvo4BVAntUERQTtgM",
        "_score": 0.8093529,
        "_source": {
          "title": "documents/car.txt",
          "content": "it was the age of wisdom, hello world I am rishabh and the age of good things.",
          "id": 15
        },
        "highlight": {
          "content": [
            "it was <span style=\"color:red;background-color:yellow;\">the age of</span> wisdom, hello world I am rishabh and <span style=\"color:red;background-color:yellow;\">the age of</span> good things."
          ]
        }
      },
      {
        "_index": "my_document_index",
        "_id": "HYsTvo4BVAntUERQvNgV",
        "_score": 0.8093529,
        "_source": {
          "title": "documents/car.txt",
          "content": "it was the age of wisdom, hello world I am rishabh and the age of good things.",
          "id": 15
        },
        "highlight": {
          "content": [
            "it was <span style=\"color:red;background-color:yellow;\">the age of</span> wisdom, hello world I am rishabh and <span style=\"color:red;background-color:yellow;\">the age of</span> good things."
          ]
        }
      },
      {
        "_index": "my_document_index",
        "_id": "HIsTvo4BVAntUERQidh4",
        "_score": 0.73261964,
        "_source": {
          "title": "documents/car.png",
          "content": "It was the best of times, it was the worst of times, it was the age of wisdom; it was the age of foolishness.",
          "id": 14
        },
        "highlight": {
          "content": [
            "It was the best of times, it was the worst of times, it was <span style=\"color:red;background-color:yellow;\">the age of</span> wisdom; it was <span style=\"color:red;background-color:yellow;\">the age of</span> foolishness"
          ]
        }
      }
    ]
  }
}
