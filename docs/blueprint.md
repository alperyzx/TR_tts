# TR_tts Technical Blueprint

## Project Architecture

### Core Components
1. **Text Processing Engine**
   - Processes Turkish text for optimal TTS delivery
   - Analyzes emphasis patterns and speech rhythm
   - Implements text normalization and SSML markup

2. **TTS Integration Layer**
   - Interfaces with Google Cloud Text-to-Speech API
   - Handles chunking for API's 5000 character limit
   - Processes API responses

3. **Audio Processing System**
   - Combines multiple MP3 fragments
   - Maintains consistent audio quality
   - Adds proper metadata

4. **Media Generation Module**
   - Creates MP4 videos from audio and images
   - Manages file format conversions

5. **Web Application**
   - Provides browser-based interface
   - Exposes API endpoints for TTS operations
   - Manages file listing and serving

## Data Flow

```
Text Input → Text Processing → TTS Conversion → Audio Processing → File Storage → Media Delivery
```

## Technical Stack
- **Backend**: Python 3.13+
- **TTS Engine**: Google Cloud Text-to-Speech
- **Web Framework**: Flask
- **Audio Processing**: pydub, mutagen, audioop-lts
- **Video Creation**: moviepy, FFmpeg
- **File Format**: MP3, MP4, WAV

## Deployment Requirements
- Python 3.13+ environment
- FFmpeg binary accessible in PATH
- Google Cloud credentials configured
- Sufficient storage for audio/video files

## Development Workflow
1. Install dependencies (`pip install -r requirements.txt`)
2. Configure Google Cloud credentials
3. Set up directories in variables.cfg
4. Run local development server with `python app.py`

## Future Enhancements
- Implement caching to reduce API calls
- Add batch processing capabilities
- Integrate additional TTS providers
- Create automated testing framework