from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import expr
from pyspark.sql.types import StringType
from pyspark.sql.streaming import DataStreamWriter
from textblob import TextBlob
import json
from pyspark.sql.types import ArrayType, StringType
import spacy

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Set up Spark session

spark = SparkSession.builder.appName("KafkaConsumer").getOrCreate()

#spark = SparkSession.builder.appName("TwitterSentimentAnalysis").config("spark.executor.memory", "2g").config("spark.driver.memory", "1g").getOrCreate()

# Set up Kafka consumer
topic_name = 'twitter_stream'

# Create a DataFrame representing the stream of input lines from Kafka
kafka_stream_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", topic_name)
    .load()
)


# Define sentiment analysis function
def analyze_sentiment(tweet_text):
    tweet_text = str(tweet_text)
    tweet_json = json.loads(tweet_text)
    tweet = tweet_json.get("tweet_text", "")
   # Ensure tweet is a string before analysis
    if isinstance(tweet, str):
        analysis = TextBlob(tweet)
        
        # Classify the polarity as 'Positive', 'Neutral', or 'Negative'
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'
    else:
        # Return None for non-string tweets
        return None

# Define competitor extraction function using spaCy
def extract_competitors(tweet_text):
    # Convert tweet_text to string
    tweet_text = str(tweet_text)

    # Parse tweet_text as JSON
    tweet_json = json.loads(tweet_text)
    tweet = tweet_json.get("tweet_text", "")

    # Ensure tweet is a string before extraction
    if isinstance(tweet, str):
        doc = nlp(tweet)
        competitors = [ent.text for ent in doc.ents if ent.label_ == "ORG"]


        # Join competitors into a single string separated by commas
        competitors_str = ", ".join(competitors) if competitors else None

        return competitors_str  # Return None if the list is empty
    else:
        # Return None for non-string tweets
        return None

# Define competitor extraction function using spaCy
def extract_competitors(tweet_text):
    # Convert tweet_text to string
    tweet_text = str(tweet_text)

    # Parse tweet_text as JSON
    tweet_json = json.loads(tweet_text)
    tweet = tweet_json.get("tweet_text", "")

    # Ensure tweet is a string before extraction
    if isinstance(tweet, str):
        doc = nlp(tweet)
        competitors = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

        # Return competitors as a list
        return competitors if competitors else None
    else:
        # Return None for non-string tweets
        return None

# Register the sentiment analysis function as a Spark UDF
sentiment_udf = udf(analyze_sentiment, StringType())
competitors_udf = udf(extract_competitors, ArrayType(StringType()))


# Apply sentiment analysis to the tweet text column
#processed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as tweet").select("tweet", sentiment_udf("tweet").alias("sentiment"))
processed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as tweet").select("tweet", sentiment_udf("tweet").alias("sentiment"), competitors_udf("tweet").alias("competitors"))


# Extract fields from the tweet JSON string
parsed_stream_df = (
    processed_stream_df
    .withColumn("tweet_data", expr("from_json(tweet, 'id INT, company_name STRING, tweet_text STRING')"))
    .select("tweet_data.*", "sentiment", "competitors")
)

# Define the MongoDB connection options
mongo_options = {
    "spark.mongodb.output.uri": "mongodb://localhost:27017/twitter_db.competitors"
}

# Write the streaming data to MongoDB using the com.mongodb.spark.sql.DefaultSource format
streaming_query = (
    parsed_stream_df
    .writeStream
    .outputMode("append")
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").options(**mongo_options).save())
    .start()
)

# Wait for the termination of the streaming query
streaming_query.awaitTermination()
