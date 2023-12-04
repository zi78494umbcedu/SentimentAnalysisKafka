from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import plotly.graph_objects as go


app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/twitter_db"
mongo = PyMongo(app)

@app.route("/")
def dashboard():
    # Retrieve data from MongoDB
    tweets = mongo.db.twitter_collection.find()

    # Aggregate sentiment counts
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for tweet in tweets:
        sentiment = tweet["sentiment"]
        sentiment_counts[sentiment] += 1

    # Format the timestamp for the last update
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create Plotly figures (replace this with your actual figure creation logic)
    bar_fig = create_bar_chart(sentiment_counts)
    pie_fig = create_pie_chart(sentiment_counts)
    scatter_fig = create_scatter_plot(sentiment_counts)

    return render_template(
        "dashboard.html",
        sentiment_counts=sentiment_counts,
        last_update_time=last_update_time,
        bar_fig=bar_fig,
        pie_fig=pie_fig,
        scatter_fig=scatter_fig
    )

def create_bar_chart(sentiment_counts):
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    bar_colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green
    bar_fig = go.Figure(
        data=[go.Bar(x=labels, y=values, marker=dict(color=bar_colors))],
        layout=dict(
            title=dict(text="Sentiment Distribution (Bar Chart)", font=dict(color='white')),
            paper_bgcolor='#2c3e50',  # Background color
            plot_bgcolor='#2c3e50',  # Plot area color
            xaxis=dict(title=dict(text="Sentiment", font=dict(color='white'))),
            yaxis=dict(title=dict(text="Count", font=dict(color='white'))),
            font=dict(color='white'),  # Text color
        )
    )

    return bar_fig

def create_pie_chart(sentiment_counts):
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    pie_colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green
    pie_fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, marker=dict(colors=pie_colors))],
        layout=dict(
            title=dict(text="Sentiment Distribution (Pie Chart)", font=dict(color='white')),
            paper_bgcolor='#2c3e50',  # Background color
            font=dict(color='white'),  # Text color
        )
    )

    return pie_fig

def create_scatter_plot(sentiment_counts):
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    scatter_colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green
    scatter_fig = go.Figure()

    for label, value, color in zip(labels, values, scatter_colors):
        scatter_fig.add_trace(
            go.Scatter(
                x=[label],
                y=[value],
                mode="markers",
                name=label,
                marker=dict(size=15, color=color),
                hovertemplate=f"Sentiment={label}<br>Count={value}"
            )
        )

    scatter_fig.update_layout(
        title=dict(text="Sentiment Distribution (Scatter Plot)", font=dict(color='white')),
        paper_bgcolor='#2c3e50',  # Background color
        plot_bgcolor='#2c3e50',  # Plot area color
        xaxis=dict(title=dict(text="Sentiment", font=dict(color='white'))),
        yaxis=dict(title=dict(text="Count", font=dict(color='white'))),
        legend=dict(title=dict(text="Sentiment", font=dict(color='white'))),
        font=dict(color='white'),  # Text color
    )

    return scatter_fig

if __name__ == "__main__":
    app.run(debug=True)
