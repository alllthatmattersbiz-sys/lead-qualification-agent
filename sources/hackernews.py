import requests
from datetime import datetime, timedelta

def search_hackernews_ai_jobs(keywords: list = None, max_stories: int = 500) -> list:
    """
    Search HackerNews for AI/Automation hiring posts.
    """
    
    if keywords is None:
        keywords = [
            "AI automation",
            "AI engineer",
            "AI consultant",
            "looking to hire AI",
            "need help with AI",
            "hiring AI",
            "AI developer",
            "machine learning engineer"
            "is hiring AI",
            "is hiring automation",
            "seeking AI",
            "seeking automation",
            "for hire AI",
            "for hire automation"
        ]
    
    leads = []
    
    try:
        # Get top stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url)
        story_ids = response.json()[:max_stories]
        
        print(f"Searching {len(story_ids)} stories for AI/automation jobs...")
        
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url).json()
            
            if not story or 'title' not in story:
                continue
            
            title = story['title'].lower()
            
            # Check if story matches any keyword
            matches = [kw for kw in keywords if kw.lower() in title]
            
            if matches:
                leads.append({
                    'id': story_id,
                    'title': story['title'],
                    'author': story.get('by', 'Unknown'),
                    'type': 'Story',
                    'text': story.get('text', ''),
                    'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'hn_link': f"https://news.ycombinator.com/item?id={story_id}",
                    'source': 'HackerNews',
                    'keywords_matched': ', '.join(matches),
                    'time': story.get('time')
                })
        
        # Also search comments in "Who is Hiring" thread if it exists
        print(f"Found {len(leads)} story matches. Now searching comments...")
        
        # Get comments from recent stories
        for story_id in story_ids[:100]:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url).json()
            
            if not story or 'kids' not in story:
                continue
            
            # Check if this is a hiring thread
            if story and 'title' in story:
                if 'hiring' in story['title'].lower() or 'ask hn' in story['title'].lower():
                    print(f"Found thread: {story['title']}")
                    
                    # Get comments from this thread
                    for comment_id in story['kids'][:100]:
                        comment_url = f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json"
                        comment = requests.get(comment_url).json()
                        
                        if not comment or 'text' not in comment:
                            continue
                        
                        text = comment['text'].lower()
                        
                        # Check if comment matches AI keywords
                        matches = [kw for kw in keywords if kw.lower() in text]
                        
                        if matches:
                            leads.append({
                                'id': comment_id,
                                'title': f"Comment by {comment.get('by', 'Unknown')}",
                                'author': comment.get('by', 'Unknown'),
                                'type': 'Comment',
                                'text': comment.get('text', '')[:500],
                                'url': '',
                                'hn_link': f"https://news.ycombinator.com/item?id={comment_id}",
                                'source': 'HackerNews (Comment)',
                                'keywords_matched': ', '.join(matches),
                                'time': comment.get('time')
                            })
        
        print(f"Total AI/automation leads found: {len(leads)}")
        return leads
    
    except Exception as e:
        print(f"Error searching HackerNews: {e}")
        return []