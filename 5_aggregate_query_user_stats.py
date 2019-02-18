import elasticsearch

client = elasticsearch.Elasticsearch()

try:
    response = client.search(
        index='_all',
        body={
          "aggs": {
            "user_count": {
              "significant_text": {
                "field": "user",
                "size": 100
              }
            }
          }
        },
        request_timeout=30
    )
except Exception as e:
    print(e)

for x in sorted(response['aggregations']['user_count']['buckets'], key=lambda x: x['doc_count'], reverse=True):
    print(x['doc_count'], x['key'])
