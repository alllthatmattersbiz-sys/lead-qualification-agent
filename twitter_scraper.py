import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

def search_hiring_tweets(keywords: list, max_results: int = 10) -> list:
    """
    Search Twitter for hiring/freelance keywords.
    
    Args:
        keywords: List of keywords to search (e.g., ["hiring", "looking for"])
        max_results: Max tweets to return
    
    Returns:
        List of tweet dictionaries with relevant data
    """
    
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    tweets_data = []
    
    for keyword in keywords:
        # Search query: keyword + exclude retweets
        query = f"{keyword} -is:retweet lang:en"
        
        try:
            tweets = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'verified']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    # Find user info from includes
                    user = None
                    if tweets.includes and 'users' in tweets.includes:
                        user = next((u for u in tweets.includes['users'] if u.id == tweet.author_id), None)
                    
                    tweets_data.append({
                        'tweet_id': tweet.id,
                        'text': tweet.text,
                        'username': user.username if user else 'Unknown',
                        'name': user.name if user else 'Unknown',
                        'created_at': tweet.created_at,
                        'keyword': keyword,
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count']
                    })
        
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
    
    return tweets_data


def get_hiring_tweets():
    """
    Main function to get hiring-related tweets.
    """
    keywords = [
        "hiring developer",
        "looking for freelancer",
        "need help with",
        "#forhire",
        "seeking freelance"
    ]
    
    tweets = search_hiring_tweets(keywords, max_results=10)
    return tweets