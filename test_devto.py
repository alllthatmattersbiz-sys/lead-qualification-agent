import requests

# Test Dev.to API
url = "https://dev.to/api/articles?tag=jobs&per_page=50"

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    articles = response.json()
    print(f"Found {len(articles)} articles with 'jobs' tag\n")
    
    for article in articles[:5]:
        print(f"- {article.get('title')}")
        print(f"  Tags: {article.get('tag_list')}\n")

except Exception as e:
    print(f"Error: {e}")