import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

print(f"Bearer Token: {BEARER_TOKEN[:20]}...")

try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    # Simple test search
    tweets = client.search_recent_tweets(
        query="hiring",
        max_results=10
    )
    
    print(f"✅ Success! Found {len(tweets.data) if tweets.data else 0} tweets")
    
    if tweets.data:
        for tweet in tweets.data:
            print(f"- {tweet.text[:100]}")
    else:
        print("No tweets found")
        
except Exception as e:
    print(f"❌ Error: {e}")