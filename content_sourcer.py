import requests
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

TOPICS = [
    "self-development", "personal growth", "communication skills",
    "productivity", "emotional intelligence", "career advancement",
    "mindset", "habits", "success", "confidence"
]

def search_trending_topics():
    """Use AI to generate trending topic ideas based on current themes"""
    prompt = f"""You are a content strategist for a motivational YouTube channel.
    
Generate 5 trending video topic ideas in these categories: {', '.join(TOPICS)}.

For each topic, provide:
1. Core idea (one sentence)
2. Why it's trending
3. Target audience pain point

Format as JSON array with keys: idea, trend_reason, pain_point"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    
    return response.choices[0].message.content

def select_best_topic(topics_json):
    """Select the most promising topic"""
    prompt = f"""From these topics, select the ONE with highest viral potential for a 60-second motivational video:

{topics_json}

Return only the core idea as a single sentence."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def source_content():
    """Main function to source trending content"""
    print("🔍 Sourcing trending topics...")
    topics = search_trending_topics()
    print(f"✓ Found trending topics")
    
    best_topic = select_best_topic(topics)
    print(f"✓ Selected topic: {best_topic}")
    
    return best_topic
