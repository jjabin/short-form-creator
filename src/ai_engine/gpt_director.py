from typing import List, Dict, Optional
from openai import OpenAI
import json

class GPTDirector:
    """AI director for content strategy and creation."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def generate_content_strategy(self, transcript: str, video_metadata: Dict) -> Dict:
        """Generate comprehensive content strategy similar to Opus.pro."""
        prompt = f"""
        As an AI content director, analyze this video transcript and metadata to create a multi-platform content strategy.
        Video Duration: {video_metadata.get('duration')}s
        Original Platform: {video_metadata.get('platform')}
        
        Transcript:
        {transcript}
        
        Provide a detailed strategy including:
        1. Key moments and timestamps for short-form content
        2. Platform-specific recommendations (TikTok, Instagram, YouTube Shorts)
        3. Suggested hooks and titles
        4. Thumbnail design recommendations
        5. Hashtag strategy
        6. Optimal posting schedule
        7. Engagement prompts
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert content strategist."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def generate_hooks(self, context: str, platform: str) -> List[str]:
        """Generate attention-grabbing hooks for different platforms."""
        prompt = f"""
        Create 5 engaging hooks for {platform} based on this context:
        {context}
        
        Hooks should be:
        - Platform-appropriate ({platform} style)
        - Attention-grabbing
        - Natural and conversational
        - Optimized for viewer retention
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an expert {platform} content creator."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return [line.strip() for line in response.choices[0].message.content.split('\n') if line.strip()]