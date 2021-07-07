# Ranking-of-social-media-nodes-and-detection-of-hate-speech

## Ranking of social media nodes

The edge list of Facebook social circles from the SNAP website has been used.

Code file named gen_centrality.py contains functions to compute the following centrality metrics for a graph:
1) Closeness Centrality
2) Betweenness Centrality
3) Biased PageRank

Code file named analyze_centrality.py contains in-built functions to compute the above mentioned centrality metrics and compares it with the user defined functions and returns how many nodes overlap.


## Detection of hate speech

### Dataset:

train.tsv: This file contains the data for training purposes. Each line represents a tweet with 3 columns, separated by tabs ( \t ). The first column is a unique identifier, the second column contains the tweet text, and the third contains the label of whether the tweet is hate speech (1) or not (0). There are 16,112 tweets in this file.

test.tsv: This file contains the data that the model should predict. It has the same format as before, but with only the first two columns. Thereare 5,000 tweets in this file.

### Generic Classifiers:

Firstly we preprocess the tweet texts to make them easier to work with. We preprocess the texts in train.tsv and test.tsv by removing punctuations and lowercasing all characters. Then we try three types of classifiers:
1) TFIDF with Random Forest Classifier
2) Word2Vec Embeddings with SVM Classifier
3) Supervised FastText
