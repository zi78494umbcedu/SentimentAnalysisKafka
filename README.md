# SentimentAnalysisKafka
A Data Intensive Application to analyze sentiments for positive/negative/neutral of Twitter APIs

This project is a good starting point for those who have little or no experience with Kafka & Apache Spark Streaming.

Input data: Tweets with a company names
Main model: Data Intensive application that can scale and run efficiently with data models and encoding schemes. Preprocessing and apply sentiment analysis on the tweets
Output: Text with all the tweets and their sentiment analysis and competitor names

We use Python version 3.11 and Spark version 3.5.0 and Kafka 3.6.0.

## Part 1: Ingest Data using Kafka 

This part is about sending tweets from Twitter Sentiment Analysis data. To do this, follow the instructions about the ingestion of Data using Kafka. 

## Part 2: Tweet preprocessing and sentiment analysis
In this part, we receive tweets from Kafka and preprocess them with the pyspark library which is python's API for spark. We then apply sentiment analysis using textblob; A python's library for processing textual Data. And have competitors names extracted using spacy library. 

After sentiment analysis, we write the sentiment analysis and competitor names in the dashboard using Flask applicaiton. We have also the possibility to store in a parquet file, which is a data storage format.
