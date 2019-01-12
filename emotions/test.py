from elasticsearch import Elasticsearch


es = Elasticsearch()

tweet = {"index": "tweets",
         "user_mentions": [],
         "@timestamp": "2018-12-10T15:41:05.000Z",
         "client": "<a href=\"http:\\twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
         "user": "RT_Deutsch",
         "retweeted": False,
         "symbols": [],
         "hashtags": [{"indices": [46, 53], "text": "Brexit"}],
         "message": "I like Brexit so much",
         "source": "http://twitter.com/RT_Deutsch/status/1072154242050387968"}

resp = es.index(index='logstash-001', doc_type="doc", body=tweet, id=1)
print(resp)


# {'_index': 'logstash-2018.12.10',
#  '_type': 'doc',
#  '_id': 'AcTHmGcBzP5sz11OgT1q',
#  '_score': None,
#  '_source':
#      {'@version': '1',
#       'user_mentions': [],
#       '@timestamp': '2018-12-10T15:41:05.000Z',
#       'client': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>',
#       'user': 'RT_Deutsch',
#       'retweeted': False,
#       'symbols': [],
#       'urls': ['https://deutsch.rt.com/europa/80815-wegen-drohender-niederlage-theresa-may-setzt-brexit-abstimmung-aus/'],
#       'hashtags': [{'indices': [46, 53], 'text': 'Brexit'}],
#       'message': 'Wegen drohender Niederlage: Theresa May setzt #Brexit-Abstimmung aus\nhttps://t.co/BgwoF2JMOL',
#       'source': 'http://twitter.com/RT_Deutsch/status/1072154242050387968'},
#  'sort': [0]}
