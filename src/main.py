import argparse
import os
from typing import List, Dict
from video_processor import VideoProcessor
from content_analyzer import ContentAnalyzer
from clip_generator import ClipGenerator

def parse_args():
    parser = argparse.ArgumentParser(description='Generate short-form content from videos')
    parser.add_argument('--input', required=True, help='Input video path or URL')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--num_clips', type=int, default=5, help='Number of clips to generate')
    parser.add_argument('--min_duration', type=float, default=15.0, help='Minimum clip duration')
    parser.add_argument('--max_duration', type=float, default=60.0, help='Maximum clip duration')
    return parser.parse_args()

async def main():
    args = parse_args()
    
    # Initialize processors
    video_proc = VideoProcessor(args.input)
    content_analyzer = ContentAnalyzer(os.getenv('OPENAI_API_KEY'))
    clip_generator = ClipGenerator(args.input)
    
    try:
        # Detect scenes
        print('Detecting scenes...')
        scenes = video_proc.detect_scenes()
        
        # Transcribe video
        print('Transcribing audio...')
        transcription = content_analyzer.transcribe_audio(args.input)
        
        # Analyze content
        print('Analyzing content...')
        analysis = await content_analyzer.analyze_content(transcription['text'])
        
        # Generate clips
        os.makedirs(args.output, exist_ok=True)
        
        for i in range(args.num_clips):
            print(f'Generating clip {i + 1}/{args.num_clips}...')
            
            # Select scene
            scene = scenes[i % len(scenes)]
            
            # Generate clip
            output_path = os.path.join(args.output, f'clip_{i + 1}.mp4')
            clip_generator.create_short(
                start_time=scene[0],
                end_time=scene[1],
                output_path=output_path
            )
    
    finally:
        # Cleanup
        video_proc.close()
        clip_generator.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())