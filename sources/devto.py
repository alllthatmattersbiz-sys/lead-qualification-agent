import requests

def get_devto_job_posts(keywords: list = None) -> list:
    """
    Scrape Dev.to job listings.
    Dev.to has job postings at dev.to/jobs
    """
    
    if keywords is None:
        keywords = [
            "AI automation",
            "AI engineer", 
            "AI consultant",
            "machine learning",
            "AI developer"
        ]
    
    try:
        # Dev.to job search
        leads = []
        
        for keyword in keywords:
            # Dev.to search API for jobs
            url = "https://dev.to/api/articles"
            
            params = {
                'state': 'published',
                'search': keyword,
                'per_page': 30
            }
            
            response = requests.get(url, params=params)
            articles = response.json()
            
            for article in articles:
                # Filter for job-related content
                tags = article.get('tag_list', [])
                title = article.get('title', '').lower()
                
                # Check if it's job-related
                if 'job' in tags or 'hiring' in tags or 'career' in tags:
                    if keyword.lower() in title or keyword.lower() in article.get('description', '').lower():
                        leads.append({
                            'id': article.get('id'),
                            'title': article.get('title'),
                            'author': article.get('user', {}).get('name', 'Unknown'),
                            'type': 'Job Post',
                            'text': article.get('description', '')[:500],
                            'url': article.get('url'),
                            'hn_link': article.get('url'),
                            'source': 'Dev.to',
                            'keywords_matched': keyword,
                            'time': article.get('published_at')
                        })
        
        return leads
    
    except Exception as e:
        print(f"Error scraping Dev.to: {e}")
        return []