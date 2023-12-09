#!/bin/bash

# Install Java
sudo apt-get update
sudo apt-get install -y default-jdk

# Install Python
sudo apt-get install -y python3 python3-pip

# Install Kafka
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xzf kafka_2.13-2.8.0.tgz
cd kafka_2.13-2.8.0
./bin/zookeeper-server-start.sh config/zookeeper.properties &
./bin/kafka-server-start.sh config/server.properties &

# Install Gradle
sudo apt-get install -y gradle

# Install Spark
wget https://downloads.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
tar -xzf spark-3.2.0-bin-hadoop3.2.tgz

# Install Flask
pip3 install Flask

# Install MongoDB
sudo apt-get install -y mongodb

# Install required Python packages
pip3 install pymongo kafka-python

# Run Zookeeper
./bin/zookeeper-server-start.sh config/zookeeper.properties &

# Run Kafka server
./bin/kafka-server-start.sh config/server.properties &

# Run Flask Dashboard application
cd path/to/your/flask/app
python3 app.py &

# Run Kafka Producer
python3 producer.py

#Run Kafka Consumer(For Mongo persistence - stream/batch processing, For Dashboard streaming)
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,net.snowflake:snowflake-jdbc:3.12.12,net.snowflake:spark-snowflake_2.12:2.9.0-spark_3.0 consumer.py

#Run Kafka Consumer For Data Warehouse -> OLAP)
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,net.snowflake:snowflake-jdbc:3.12.12,net.snowflake:spark-snowflake_2.12:2.9.0-spark_3.0 consumerOLAP.py


# Setting up environment for OLAP for new packages
pip3 install --force-reinstall pyspark==3.4
#Might have to donwgrade from spark3.5 to spark3.4 due to incompatible snowflake and JDBC versions
spark-shell --packages net.snowflake:snowflake-jdbc:3.9.2,net.snowflake:spark-snowflake_2.12:2.13.0-spark_3.4
