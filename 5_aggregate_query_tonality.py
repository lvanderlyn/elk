import elasticsearch

client = elasticsearch.Elasticsearch()

try:
    response = client.search(
        index='_all',
        body={
          "aggs": {
            "tonality": {
              "significant_text": {
                "field": "tonality_13"
              }
            }
          }
        },
        request_timeout=30
    )
except Exception as e:
    print(e)

for x in sorted(response['aggregations']['tonality']['buckets'], key=lambda x: x['doc_count'], reverse=True):
    print(x['doc_count'], x['key'])
