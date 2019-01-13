# elk

GOALS: 

Text technology project 2018, working with elastic search to complete an interesting downstream NLP task

In this project we made use of the tools logstash and elasticsearch to agregate
and process tweets about Brexit. We used the logstash twitter tool to search for
the keyword 'Brexit'. These tweets were then converted into JSON and stored in
our elasticsearch instance. 

Our goal with this project was to analyze the tweets to determine if we could
classify the emotion and partisanship (pro-Brexit, anti-Brexit, or neutral) of the
writer.

To accomplish this, we use query elastic search for a random sample of tweets
(generate_annotation_samples()) to hand-annotate and perform classification as
an outside module (see emotion and partisanship folders).


DIRECTORY ORGANISATION:
	* /emotions      -> contains code related to classifying and labeling
	                    emotions to tweet data in elastic search
	* /partisanship  -> contains code related to classifying and labeling
	                    the authors side in the Brexit debate
	* /topicModeling -> contains code related to classifying and labeling
	                    arguments used in pro/anti-Brexit posts
	* /config        -> contains configuration file for logstash 

	* /lib/elasticsearch -> contains configuration for elasticsearch
	                        instance
	* /lib/classifiers   -> contains the machine learning classifiers used
	                        classifying partisanship and topics

