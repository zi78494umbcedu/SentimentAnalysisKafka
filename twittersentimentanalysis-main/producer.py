import pandas as pd
from kafka import KafkaProducer

import json
import time

# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'twitter_stream'

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load static training dataset from Kaggle
training_data = pd.read_csv('/Users/ashwingupta/Desktop/SENG-691_Data_Intensive_Applications/Git1/twittersentimentanalysis-main/archive/twitter_training.csv', header=None, names=['id', 'company_name', 'sentiment', 'tweet_text'])

class TweetProducer:

    def __init__(self, producer, topic_name):
        self.producer = producer
        self.topic_name = topic_name

    def produce_tweets(self, data):
        for _, row in data.iterrows():
            tweet = {
                "id": row["id"],
                "company_name": row["company_name"],
                "sentiment": row["sentiment"],
                "tweet_text": row["tweet_text"]
                # Add more fields as needed
            }
            self.producer.send(self.topic_name, value=tweet)
            print("Tweet sent to Kafka: {}".format(tweet))
            time.sleep(1)  # Simulate streaming by adding a delay

if __name__ == '__main__':
    # Create a TweetProducer instance
    tweet_producer = TweetProducer(producer, topic_name)

    # Produce tweets from the static dataset
    while True:
        tweet_producer.produce_tweets(training_data)
        # Sleep for 10 minutes before producing the next batch
        time.sleep(600)
