import requests

def search_github_hiring_issues(keywords: list = None) -> list:
    """
    Search GitHub for hiring/recruitment issues.
    Looks for "hiring", "looking for", etc.
    """
    
    if keywords is None:
        keywords = [
            "hiring AI",
            "looking for developer",
            "seeking freelancer",
            "AI consultant needed"
            "need help with AI",
            "hiring automation",
            "looking for automation",
            "seeking automation",
            "for hire AI",
            "for hire automation"   
        ]
    
    try:
        leads = []
        
        for keyword in keywords:
            # GitHub search API
            search_query = f'"{keyword}" type:issue is:open'
            url = "https://api.github.com/search/issues"
            
            params = {
                'q': search_query,
                'sort': 'updated',
                'order': 'desc',
                'per_page': 10
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                for issue in results.get('items', []):
                    # Filter for actual hiring posts (not spam)
                    body = issue.get('body', '').lower()
                    title = issue.get('title', '').lower()
                    
                    if 'budget' in body or 'hire' in title or 'freelance' in body:
                        leads.append({
                            'id': issue.get('id'),
                            'title': issue.get('title'),
                            'author': issue.get('user', {}).get('login', 'Unknown'),
                            'type': 'GitHub Issue',
                            'text': issue.get('body', '')[:500],
                            'url': issue.get('html_url'),
                            'hn_link': issue.get('html_url'),
                            'source': 'GitHub',
                            'keywords_matched': keyword,
                            'time': issue.get('updated_at')
                        })
        
        return leads
    
    except Exception as e:
        print(f"Error searching GitHub: {e}")
        return []