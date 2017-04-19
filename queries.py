from elasticsearch import Elasticsearch
es = Elasticsearch()

index = 'xenmbox'

# Number of messages on an unknown thread.
count = es.count(index=index, doc_type='unknown')
print(str(count['count']))

# All Message-IDs.
body = {
        "aggs": {
            "message_ids": {
                "terms": {
                    "field": "data.Message-ID",
                    "size": 5000
                }
            }
        }
}

response = es.search(index=index, body=body)
print(str(response['aggregations']['message_ids']['buckets']))

