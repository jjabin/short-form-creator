import numpy as np
from typing import List, Dict, Tuple
from openai import OpenAI

class ContentScorer:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    async def score_segments(self, 
                           segments: List[Dict],
                           transcription: str) -> List[Dict]:
        """Score video segments based on content engagement potential."""
        
        prompt = f"""Analyze this video transcript and rate each segment for short-form content potential.
        Consider factors like:
        - Entertainment value
        - Key information density
        - Emotional impact
        - Stand-alone coherence
        
        Transcript:
        {transcription}
        
        For each segment, provide a score from 0-100 and brief explanation."""

        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in viral short-form content creation."},
                {"role": "user", "content": prompt}
            ]
        )

        # Process GPT-4 analysis into segment scores
        analysis = response.choices[0].message.content
        scored_segments = self._parse_gpt_analysis(analysis, segments)
        
        return scored_segments

    def _parse_gpt_analysis(self, analysis: str, segments: List[Dict]) -> List[Dict]:
        """Parse GPT analysis into numerical scores for segments."""
        # Add basic scoring logic here
        scored_segments = []
        for i, segment in enumerate(segments):
            # Extract score from analysis (implement parsing logic)
            estimated_score = np.random.uniform(60, 100)  # Placeholder
            
            scored_segments.append({
                **segment,
                'engagement_score': estimated_score,
                'analysis': f'Segment {i+1} analysis'  # Extract from GPT response
            })
        
        return scored_segments

    def select_best_segments(self, 
                           scored_segments: List[Dict], 
                           num_clips: int,
                           min_duration: float = 15.0,
                           max_duration: float = 60.0) -> List[Dict]:
        """Select the best segments for short-form content."""
        
        # Filter segments by duration
        valid_segments = [
            seg for seg in scored_segments
            if min_duration <= (seg['end_time'] - seg['start_time']) <= max_duration
        ]
        
        # Sort by engagement score
        sorted_segments = sorted(
            valid_segments,
            key=lambda x: x['engagement_score'],
            reverse=True
        )
        
        return sorted_segments[:num_clips]
