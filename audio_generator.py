import requests
import os
import config

def generate_audio(script, output_path):
    """Generate voiceover using ElevenLabs API"""
    
    if not config.ELEVENLABS_API_KEY:
        print("⚠️  ElevenLabs API key not set, using OpenAI TTS")
        return generate_audio_openai(script, output_path)
    
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": config.ELEVENLABS_API_KEY
    }
    
    data = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Audio generation failed: {response.text}")

def generate_audio_openai(script, output_path):
    """Fallback: Generate audio using OpenAI TTS"""
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=script
    )
    
    response.stream_to_file(output_path)
    return output_path

def create_audio(script, video_id):
    """Main function to create audio"""
    print("🎙️  Generating voiceover...")
    
    os.makedirs(config.AUDIO_DIR, exist_ok=True)
    output_path = f"{config.AUDIO_DIR}/video_{video_id}.mp3"
    
    audio_path = generate_audio(script, output_path)
    print(f"✓ Audio created: {audio_path}")
    
    return audio_path
