# elk

GOALS: 

Text technology project 2018, working with elastic search to complete an
interesting downstream NLP task.

In this project we made use of the tools logstash and elasticsearch to aggregate
and process tweets about Brexit. We used logstash with the official twitter
plugin to search for the keyword 'Brexit'. These tweets were then converted
into JSON and stored in our elasticsearch instance. 

Our goal with this project was to analyze the tweets to determine if we could
classify the emotion and partisanship (pro-Brexit, anti-Brexit, or neutral) of
the writer.

To accomplish this, we query elastic search for a random sample of tweets
(generate_annotation_samples.py) to hand-annotate and perform classification as
an outside module (see emotion and partisanship folders).


DIRECTORY ORGANISATION:
 Scripts:
	* 2_classifier.py                -> classifies tweets as pro/anti-Brexit
	                                    or neutral
	* 3_topic_modeling.py            -> clusters tweets by topic
	* 4_load_model_predict.py        -> classifies tweets as positive or
	                                    negative
	* generate_annotation_samples.py -> generates a random sample of tweets
	                                    to be hand-annotated
 Directories:
	* /emotions      -> contains code for classifying and labeling
	                    emotions of tweet data in elastic search
	* /partisanship  -> contains code related to classifying and labeling
	                    the authors side in the Brexit debate
	* /config        -> contains configuration file for logstash 

 	* /lib/elasticsearch -> contains configuration for elasticsearch
	                        instance
	* /lib/classifiers   -> contains the machine learning classifiers used
	                        classifying partisanship and topics

