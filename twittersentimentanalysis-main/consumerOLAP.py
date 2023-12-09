from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import expr
from pyspark.sql.types import StringType
from pyspark.sql.streaming import DataStreamWriter
from textblob import TextBlob
import json
from pyspark.sql.types import ArrayType, StringType
import spacy
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date
from pyspark.sql.functions import count
from pyspark.sql.functions import date_format
from pyspark.sql.functions import current_timestamp

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Set up Spark session

spark = SparkSession.builder.appName("KafkaConsumer").getOrCreate()

#MONGO
'''spark = SparkSession.builder.appName("TwitterSentimentAnalysis").config("spark.executor.memory", "2g").config("spark.driver.memory", "1g").getOrCreate()'''

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


#MONGO Apply sentiment analysis to the tweet text column
#processed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as tweet").select("tweet", sentiment_udf("tweet").alias("sentiment"))
'''processed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as tweet").select("tweet", sentiment_udf("tweet").alias("sentiment"), competitors_udf("tweet").alias("competitors"))
'''

#MONGO Extract fields from the tweet JSON string
'''parsed_stream_df = (
    processed_stream_df
    .withColumn("tweet_data", expr("from_json(tweet, 'id INT, company_name STRING, tweet_text STRING')"))
    .select("tweet_data.*", "sentiment", "competitors")
)'''

#MONGO Define the MongoDB connection options
mongo_options = {
    "spark.mongodb.output.uri": "mongodb://localhost:27017/twitter_db.competitors"
}

#MONGO Write the streaming data to MongoDB using the com.mongodb.spark.sql.DefaultSource format
'''streaming_query = (
    parsed_stream_df
    .writeStream
    .outputMode("append")
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").options(**mongo_options).save())
    .start()
)
'''


#SNOWFLAKE - DATA WAREHOUSE - OLAP
#SNOWFLAKE - DATA WAREHOUSE - OLAP
#SNOWFLAKE - DATA WAREHOUSE - OLAP
#SNOWFLAKE - DATA WAREHOUSE - OLAP

#Spark Connection Builder with Snowflake and JDBC 
spark = SparkSession.builder \
    .appName("KafkaConsumerWithSnowflake") \
    .config("spark.jars.packages", "file:///Users/ashwingupta/.ivy2/jars/snowflake-jdbc-3.9.2.jar,file:///Users/ashwingupta/.ivy2/jars/net.snowflake_spark-snowflake_2.12-2.12.0-spark_3.4.jar") \
    .getOrCreate()

#Summary options for snowflake connection
snowflake_options = {
    "sfURL": "https://jlihyif-pra65453.snowflakecomputing.com",
    "sfDatabase": "SENTIMENT_DB",
    "sfWarehouse": "SENTIMENT_WAREHOUSE",
    "sfSchema": "PUBLIC",
    "sfRole": "ACCOUNTADMIN",
    "sfuser":"ZI78494",
    "sfpassword":"Muskan@98",
    "dbtable": "SENTIMENT_ANALYSIS",
    "competitors": "competitors",
    "analysis_date": "analysis_date"# Include the analysis_date column
}

#MONGO Extract fields from the tweet JSON string
'''parsed_stream_df = (
    processed_stream_df
    .withColumn("tweet_data", expr("from_json(tweet, 'id INT, company_name STRING, tweet_text STRING')"))
)'''
# Apply sentiment analysis and competitor extraction to the tweet text column
processed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING) as tweet")\
    .select("tweet", sentiment_udf("tweet").alias("sentiment"), competitors_udf("tweet").alias("competitors"))

# Extract fields from the tweet JSON string
parsed_stream_df = processed_stream_df\
    .withColumn("tweet_data", expr("from_json(tweet, 'id INT, company_name STRING, tweet_text STRING')"))\
    .select("tweet_data.id",  "tweet_data.company_name", "sentiment","tweet_data.tweet_text", "competitors")\
    .withColumn("analysis_date", date_format(current_timestamp(), "yyyy-MM-dd HH:mm:ss"))


# Add analysis_date to your DataFrame
#parsed_stream_df = parsed_stream_df.withColumn("analysis_date", current_date())

parsed_stream_df = parsed_stream_df.withColumn("analysis_date", current_timestamp())

streaming_query = (
    parsed_stream_df
    .writeStream
    .outputMode("append")
    .format("net.snowflake.spark.snowflake")
    .options(**snowflake_options)
    .foreachBatch(lambda batch_df, batch_id: batch_df.write
                 .format("net.snowflake.spark.snowflake")
                 .options(**snowflake_options)
                 .mode("append")
                 .save())
    .start()
)

# Wait for the termination of the streaming query
streaming_query.awaitTermination()
'''
#Spark DataFrame named aggregated_stream_df
#Spark DataFrame named aggregated_stream_df
#Spark DataFrame named aggregated_stream_df
#Spark DataFrame named aggregated_stream_df
#Spark DataFrame named aggregated_stream_df
# Define Snowflake connection options for DailySummary
daily_summary_options = {
    "sfURL": "https://jlihyif-pra65453.snowflakecomputing.com",
    "sfDatabase": "SENTIMENT_DB",
    "sfWarehouse": "SENTIMENT_WAREHOUSE",
    "sfSchema": "PUBLIC",
    "sfRole": "ACCOUNTADMIN",
    "sfuser":"ZI78494",
    "sfpassword":"Muskan@98",
    "dbtable": "DAILYSUMMARY",
    "analysis_date": "analysis_date"# Include the analysis_date column
}
aggregated_stream_df = (parsed_stream_df.withWatermark("analysis_date", "1 day").groupBy("analysis_date", "sentiment", "competitors").agg(count("*").alias("mention_count")))
aggregated_stream_df.createOrReplaceTempView("aggregated_stream_view")
# Create a new DataFrame with the desired columns
insert_df = aggregated_stream_df.select("analysis_date", "sentiment", "competitors", "mention_count")
# Write aggregated data to Snowflake DailySummary table
try:
    spark.sql(f"CREATE TABLE IF NOT EXISTS {daily_summary_options['sfDatabase']}.{daily_summary_options['sfSchema']}.{daily_summary_options['dbtable']} (analysis_date TIMESTAMP, sentiment STRING, competitors STRING, mention_count LONG)")
except Exception as e:
    print(f"Error creating table: {e}")
# Insert data into the Snowflake DailySummary table
# Write aggregated data to Snowflake DailySummary table
# Write aggregated data to Snowflake DailySummary table
query = (
    aggregated_stream_df
    .writeStream
    .outputMode("append")
    .format("net.snowflake.spark.snowflake")
    .options(**daily_summary_options)
    .start()
)
# Write aggregated data to Snowflake DailySummary table
spark.sql("""INSERT INTO DAILYSUMMARY (AnalysisDate, Sentiment, Competitor, MentionCount) SELECT analysis_date, sentiment, competitors, COUNT(*) as MentionCount FROM aggregated_stream_view GROUP BY analysis_date, sentiment, competitors""").write.format("net.snowflake.spark.snowflake").options(**daily_summary_options).mode("append").save().start()'''
