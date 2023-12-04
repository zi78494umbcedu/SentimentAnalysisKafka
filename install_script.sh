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
