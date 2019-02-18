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
the writer as well as the main arguments (both for and against used).

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

	* /emotions_model      -> contains code for training a model for
	                          classifying emotions of tweet data. And
	                          contains a saved trained model
	* /partisanship        -> contains code related to classifying and 
	                          labeling the authors side in the Brexit debate
	* /config              -> contains configuration file for logstash 

 	* /lib/elasticsearch -> contains configuration for elasticsearch
	                        instance
	* /lib/classifiers   -> contains the machine learning classifiers used
	                        classifying partisanship and topics

 Work in Kibana:
 
   * Generating bar graph:
     * Used count() functionality to count the number of posts by user.keyword
     * Graphhed counts/user
   * Generating word cloud:
     * Made a word cloud of most common hashtags
     * Explored filtering by user and by content of tweet
   * Generating sentiment Pie charts:
     * Added sentiment data we calculated to elasticsearch then plotted
       percent postive/negative
     * Explored how this changed between specific users (those who posted a lot)
     * Explored how this changed for tweets containing specific words 
       ("hate", "remain", "leave", "pain", etc)
     * Tried to plot top 100 posters, but had trouble because of elasticsearch's 
       weakness with aggregation
   * Generated Timelion graphic for post counts
     * Plotted number of posts against time for the period we collected data
   * Generated Dashboard from visualisations
     * Explored fuzzy search and full text search and proximity search