import numpy as np
from pyannote.audio import Pipeline

class SpeakerDetector:
    def __init__(self, auth_token):
        self.pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization',
            use_auth_token=auth_token
        )
    
    def detect_speakers(self, audio_path):
        """Detect and track speakers in audio"""
        diarization = self.pipeline(audio_path)
        
        speakers = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speakers.append({
                'start': turn.start,
                'end': turn.end,
                'speaker': speaker
            })
            
        return speakers
    
    def get_active_speaker(self, timestamp, speakers):
        """Get active speaker at a specific timestamp"""
        for speaker in speakers:
            if speaker['start'] <= timestamp <= speaker['end']:
                return speaker['speaker']
        return None