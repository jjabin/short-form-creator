# Short Form Creator

An AI-powered tool for automatically converting long-form videos into engaging short-form content. This tool uses GPT-4 for content understanding, Whisper for transcription, and computer vision for scene detection and analysis.

## Features

- Automatic video downloading (YouTube support)
- Speech-to-text transcription with timestamps
- AI-powered content analysis and interesting moment detection
- Smart scene detection and clip extraction
- Vertical video reformatting with smart cropping
- Caption generation and overlay
- Background music integration
- Batch processing capability

## Installation

```bash
git clone https://github.com/jjabin/short-form-creator.git
cd short-form-creator
pip install -r requirements.txt
```

## Usage

1. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. Run the clipper:
```bash
python main.py --input "video_url_or_path" --output "output_directory" --num_clips 5
```

## Configuration

Edit `config.py` to customize:
- Clip duration limits
- Content filters
- Output format preferences
- AI model settings

## Requirements

- Python 3.8+
- FFmpeg
- OpenAI API key

## How It Works

1. **Video Analysis**
   - Scene detection using computer vision
   - Content understanding with GPT-4
   - Key moment identification

2. **Clip Generation**
   - Smart vertical cropping
   - Caption generation
   - Background music integration

3. **Post-processing**
   - Format optimization
   - Quality enhancement
   - Metadata generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.