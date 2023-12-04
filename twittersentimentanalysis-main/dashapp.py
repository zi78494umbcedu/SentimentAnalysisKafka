from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime
import plotly.graph_objects as go

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/twitter_db"
mongo = PyMongo(app)

def get_dynamic_data():
    # Replace this with your actual MongoDB query logic
    tweets = mongo.db.competitors.find()
    return list(tweets)

@app.route("/")
def dashboard():
    # Retrieve data from MongoDB
    tweets_data = get_dynamic_data()

    # Check if "sentiment" field is present in each tweet
    tweets_with_sentiment = [tweet for tweet in tweets_data if "sentiment" in tweet]
    
    # Extract necessary information for display
    sentiments = [tweet["sentiment"] for tweet in tweets_with_sentiment]

    # Check if the "competitors" field is present and not empty
    tweets_with_competitors = [tweet for tweet in tweets_with_sentiment if "competitors" in tweet and tweet["competitors"]]
    
    # Extract competitors as a list of strings
    competitors = []
    for tweet in tweets_with_competitors:
        competitors.extend(tweet["competitors"])

    # Aggregate sentiment counts
    sentiment_counts = {"Positive": sentiments.count("Positive"),
                        "Neutral": sentiments.count("Neutral"),
                        "Negative": sentiments.count("Negative")}

    # Aggregate competitor mentions
    competitor_mentions = {}
    for competitor in competitors:
        if competitor in competitor_mentions:
            competitor_mentions[competitor] += 1
        else:
            competitor_mentions[competitor] = 1

    # Format the timestamp for the last update
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create Plotly figures (replace this with your actual figure creation logic)
    bar_fig_sentiment = create_bar_chart(
    sentiment_counts,
    chart_title="Sentiment Distribution",
    x_axis_title="Sentiment",
    y_axis_title="Count",
    width=600,  # Adjust the width as needed
    height=400   # Adjust the height as needed
    )
    bar_fig_competitor = create_bar_chart(
        competitor_mentions,  
        chart_title="Competitor Mentions",
        x_axis_title="Competitors",
        y_axis_title="Mentions Count",
        width=1000,  # Adjust the width as needed
        height=500   # Adjust the height as needed)
    )

    return render_template(
    "dashboard1.html",
    last_update_time=last_update_time,
    bar_fig_sentiment=bar_fig_sentiment,
    bar_fig_competitor=bar_fig_competitor
)


def create_bar_chart(data, chart_title, x_axis_title, y_axis_title, width=800, height=400):
    labels = list(data.keys())
    values = list(data.values())

    # Determine the maximum width for competitor names
    max_name_length = max(len(label) for label in labels)

    # Add dots to make competitor names symmetrical
    formatted_labels = [label.ljust(max_name_length, '.') for label in labels]

    bar_colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green
    bar_fig = go.Figure(
        data=[go.Bar(x=formatted_labels, y=values, marker=dict(color=bar_colors))],
        layout=dict(
            paper_bgcolor='#2c3e50',  # Background color
            plot_bgcolor='#2c3e50',  # Plot area color
            font=dict(color='white'),  # Text color
            width=width,
            height=height,
            title=dict(text=chart_title),
            xaxis=dict(title=x_axis_title),
            yaxis=dict(title=y_axis_title),
        )
    )

    return bar_fig

if __name__ == "__main__":
    app.run(debug=True)
