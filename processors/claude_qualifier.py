import os
import json
import requests
import re


# Just get the API key directly
API_KEY = os.getenv('ANTHROPIC_API_KEY')


def qualify_lead(lead: dict) -> dict:
    """Use Claude to qualify and score a lead."""
    
    if not API_KEY:
        print("❌ ANTHROPIC_API_KEY not found")
        return {**lead, "score": 0, "explanation": "No API key", "is_qualified": False}
    
    prompt = f"""
You are an expert at qualifying AI/Automation consulting leads.

LEAD: {lead['title']} - {lead['text'][:200]}

Score 1-10. Respond ONLY as JSON (no markdown):
{{
  "score": <1-10>,
  "explanation": "<why>",
  "is_qualified": <true if >= 5>,
  "company_name": "<or Unknown>",
  "opportunity": "<what they need>",
  "budget_signal": "<money mention or Not mentioned>",
  "timeline": "<timeline or Not mentioned>",
  "contact_info": "<how to contact>",
  "email_subject": "<subject>",
  "email_opening": "<2 sentences>"
}}
"""
    
    try:
        print(f"🔄 Calling Claude for: {lead['author']}")
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 500,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        
        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            return {**lead, "score": 0, "explanation": f"API error", "is_qualified": False}
        
        data = response.json()
        response_text = data['content'][0]['text'].strip()
        
        # Strip markdown code fences if present
        response_text = re.sub(r'^```json\n?', '', response_text)
        response_text = re.sub(r'\n?```$', '', response_text)
        
        print(f"✅ Got response: {response_text[:50]}...")
        
        qualification = json.loads(response_text)
        return {**lead, **qualification}
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"   Text was: {response_text[:100]}")
        return {**lead, "score": 3, "explanation": "Parse error", "is_qualified": False}
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {**lead, "score": 0, "explanation": str(e), "is_qualified": False}


def batch_qualify_leads(leads: list) -> list:
    """Qualify multiple leads with Claude."""
    print(f"\n🚀 Starting qualification of {len(leads)} leads...\n")
    
    qualified_leads = []
    
    for i, lead in enumerate(leads):
        print(f"[{i+1}/{len(leads)}] {lead['author']}")
        qualified = qualify_lead(lead)
        qualified_leads.append(qualified)
    
    qualified_leads.sort(key=lambda x: x.get('score', 0), reverse=True)
    return qualified_leads