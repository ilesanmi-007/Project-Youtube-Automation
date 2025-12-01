from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_metadata(topic, script):
    """Generate SEO-optimized title, description, tags"""
    prompt = f"""Create YouTube metadata for this motivational video:

Topic: {topic}
Script: {script[:200]}...

Generate:
1. Title (max 60 chars, clickable, emotional)
2. Description (150-200 words, SEO-rich, with timestamps)
3. 15 relevant tags
4. 5 hashtags

Format as JSON with keys: title, description, tags, hashtags"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def create_metadata(topic, script):
    """Main function to create metadata"""
    print("🏷️  Generating SEO metadata...")
    metadata = generate_metadata(topic, script)
    print("✓ Metadata created")
    return metadata
