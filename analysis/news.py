import requests
from typing import Dict, List

NEWS_API_KEY = '0fd42d01e67d408183069bf0c006c1a8'  # Replace with your NewsAPI key

def fetch_news(symbol: str) -> List[Dict]:
    """Fetch latest news articles related to the given symbol"""
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    elif response.status_code == 401:
        print("Error fetching news: Unauthorized. Check your API key.")
    else:
        print(f"Error fetching news: {response.status_code}")
    return []

def analyze_sentiment(articles: List[Dict]) -> Dict:
    """Analyze sentiment of news articles"""
    positive, negative, neutral = 0, 0, 0
    for article in articles:
        # Simple sentiment analysis based on keywords
        title = article.get('title', '').lower()
        if any(word in title for word in ['bullish', 'positive', 'gain', 'rise']):
            positive += 1
        elif any(word in title for word in ['bearish', 'negative', 'loss', 'fall']):
            negative += 1
        else:
            neutral += 1
    
    total = positive + negative + neutral
    return {
        "positive": positive / total if total else 0,
        "negative": negative / total if total else 0,
        "neutral": neutral / total if total else 0
    }
