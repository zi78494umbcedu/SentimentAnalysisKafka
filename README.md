# SentimentAnalysisKafka
A Data Intensive Application to analyze sentiments for positive/negative/neutral of Twitter APIs

This project is a good starting point for those who have little or no experience with Kafka & Apache Spark Streaming.
<img width="591" alt="Screenshot 2023-12-03 at 11 44 45 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/8ffb3a7c-2a7c-43bd-a0fb-018dcc4d5e12">

Input data: Tweets with a company names
Main model: Data Intensive application that can scale and run efficiently with data models and encoding schemes. Preprocessing and apply sentiment analysis on the tweets
Output: Text with all the tweets and their sentiment analysis and competitor names

We use Python version 3.11 and Spark version 3.5.0 and Kafka 3.6.0.

## Part 1: Ingest Data using Kafka 

This part is about sending tweets from Twitter Sentiment Analysis data. To do this, follow the instructions about the ingestion of Data using Kafka. 

## Part 2: Tweet preprocessing and sentiment analysis
In this part, we receive tweets from Kafka and preprocess them with the pyspark library which is python's API for spark. We then apply sentiment analysis using textblob; A python's library for processing textual Data. And have competitors names extracted using spacy library. 

After sentiment analysis, we write the sentiment analysis and competitor names in the dashboard using Flask applicaiton. We have also the possibility to store in a parquet file, which is a data storage format.
<img width="759" alt="Screenshot 2023-12-03 at 11 45 05 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/2cd6533e-ea4b-4792-891a-7cac7b4743ef">
<img width="756" alt="Screenshot 2023-12-03 at 11 45 18 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/03126a63-2513-4030-8712-5640d292e760">

## Part 3: Data Warehouse (Snowflake) and OLAP (Online Analytical Processing)
A Single source of truth and an integrated, non-volatile store for historical streamed data by Spark for complex querying helping analysts for Daily/Monthly/Quarterly Summaries 
Example1: Average Sentiment Score per Company
<img width="392" alt="Screenshot 2023-12-08 at 9 20 52 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/9456f1d1-f4a1-4d53-814b-d0d41737c71c">
<img width="300" alt="Screenshot 2023-12-08 at 9 21 03 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/1d08a649-31e1-47a6-97a4-0253b584680c">

Example2: Top Competitors by Mention Count
<img width="600" alt="Screenshot 2023-12-08 at 9 22 04 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/f5fdea08-9b33-4c6d-a38c-c6afd63f367e">

Example3: Sentiment Trend Over Time/Daily Summary
<img width="601" alt="Screenshot 2023-12-08 at 9 22 22 PM" src="https://github.com/zi78494umbcedu/SentimentAnalysisKafka/assets/125627136/ecde6369-05c1-44d7-a221-43b4375e7aa2">
