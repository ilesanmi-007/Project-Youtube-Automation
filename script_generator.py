from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_script(topic):
    """Generate original, poetic motivational script"""
    prompt = f"""Create a 45-90 second motivational script about: {topic}

Requirements:
- Poetic, emotional, modern tone
- Punchy, retention-optimized
- NO clichés or overused phrases
- Safe for monetization
- Original voice and perspective
- Hook in first 3 seconds
- Clear call-to-action at end

Write ONLY the script, no titles or descriptions."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    
    script = response.choices[0].message.content.strip()
    return script

def estimate_duration(script):
    """Estimate script duration (avg 150 words per minute)"""
    words = len(script.split())
    duration = (words / 150) * 60
    return round(duration, 1)

def create_script(topic):
    """Main function to create script"""
    print(f"📝 Generating script for: {topic}")
    script = generate_script(topic)
    duration = estimate_duration(script)
    print(f"✓ Script created ({duration}s, {len(script.split())} words)")
    return script, duration
