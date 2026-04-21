import requests

# Get top stories
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url)
story_ids = response.json()[:50]

print("Top 50 HackerNews stories:\n")

for story_id in story_ids:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    story = requests.get(story_url).json()
    
    if story and 'title' in story:
        print(f"- {story['title']}")
        
        # Check if it's a hiring thread
        if 'hiring' in story['title'].lower() or 'ask hn' in story['title'].lower():
            print(f"  ✅ MATCH: {story_url}")