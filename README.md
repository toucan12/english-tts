# High-Quality TTS Program for English Learning

A program that converts English sentences from text files to high-quality MP3 files using gTTS (Google Text-to-Speech) and FFmpeg.

## Features

- ✅ **High-Quality Audio**: 44100Hz, 320kbps, stereo
- ✅ **Precise 2-Second Pause**: Exactly 2 seconds of silence added between each sentence
- ✅ **Audio Enhancement**: Volume normalization + compressor + noise filtering
- ✅ **US English**: More accurate pronunciation with en-us accent
- ✅ **Clear Voice**: Even small consonants are clearly audible

## Requirements

### 1. Python Libraries
```bash
pip install gtts
```

### 2. FFmpeg Installation (Required)

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
1. Download from [FFmpeg official site](https://ffmpeg.org/download.html)
2. Extract and add to PATH

**Installation Check:**
```bash
ffmpeg -version
```

## Usage

```bash
python english_tts.py <text_filename>
```

### Example

```bash
python english_tts.py sample.txt
```

Running the above command will create a `sample.mp3` file.

## Processing Steps

1. **Individual TTS Conversion**: Convert each sentence individually to US English
2. **High-Quality Processing**: Convert to 44100Hz, 320kbps using FFmpeg
3. **Audio Enhancement**: Apply noise removal, volume normalization, and compression
4. **2-Second Silence Insertion**: Add precise timing pauses between sentences
5. **Final Combination**: Combine all elements in high quality

## File Structure

- `english_tts.py`: Main program
- `sample.txt`: Example English sentence file
- `requirements.txt`: Required Python packages list
- `README.md`: Usage guide

## Audio Quality Improvements

### 🎵 Audio Quality Enhancement
- **Sampling Rate**: 44100Hz (CD quality)
- **Bitrate**: 320kbps (highest MP3 quality)
- **Channels**: Stereo

### 🔊 Audio Processing
- **Volume Normalization**: Maintain consistent volume using LUFS standard
- **Dynamic Compressor**: Enhance quiet sounds, moderate loud sounds
- **Noise Filtering**: Focus on 80Hz~8kHz voice frequency range

### ⏱️ Timing
- **Precise 2-Second Pause**: Real silence insertion, not text-based
- **Natural Transitions**: Smooth connections between sentences

## Text File Format

Text files should be written in the following format:
- One English sentence per line
- Empty lines are automatically ignored
- Save in UTF-8 encoding

### Example (sample.txt):
```
Hello, how are you today?
I am learning English with Python.
This is a great way to practice pronunciation.
Technology makes language learning easier.
Practice makes perfect.
Good morning, have a nice day.
Thank you for your help.
See you later, goodbye.
```

## Output Example

When running the program, the following information will be displayed:

```
📖 Reading text file: sample.txt
📝 Found a total of 8 sentences:
  1. Hello, how are you today?
  2. I am learning English with Python.
  ...

🔧 Using FFmpeg for high-quality TTS + audio enhancement...
   📊 Applied effects: 20% volume increase, compressor, noise filtering

📝 Converting 8 sentences individually to high quality... (44100Hz, 320kbps)
  🔊 1/8: Hello, how are you today?...
  🔊 2/8: I am learning English with Python...
  ...

🔗 Combining high-quality files...
✅ High-quality audio file has been created: sample.mp3
📝 Exactly 2 seconds of silence has been added between each sentence and at the end.
🎵 Audio quality: 44100Hz, 320kbps, stereo
🔊 Audio enhancement: 20% volume increase + compressor + noise filtering

🎉 Complete! Please play the 'sample.mp3' file.
```

## Troubleshooting

### FFmpeg Related Errors
If the program shows an error that FFmpeg cannot be found:

1. **Check FFmpeg Installation**:
   ```bash
   ffmpeg -version
   ```

2. **Install on macOS**:
   ```bash
   brew install ffmpeg
   ```

3. **Install on Ubuntu/Debian**:
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

### Internet Connection Required
- gTTS uses Google's online TTS service
- Internet connection is required during conversion

### Long Text Processing
- Each sentence is processed individually, so many sentences may take time
- Progress is displayed in real-time

## English Learning Applications

### 🎧 Listening Practice
- Clear distinction with 2-second pauses between sentences
- Accurate pronunciation learning with high-quality audio

### 🗣️ Repeat Practice  
- Use pauses between sentences for speaking practice
- All sounds are clearly audible with compressor

### 📝 Dictation Practice
- Consistent volume with volume normalization
- Clean audio with noise filtering

## Notes

- Internet connection is required (uses Google TTS API)
- Generated MP3 files play with US English pronunciation
- File size may be large due to highest quality settings

## Development Information

This program was written using GitHub Copilot Agent mode with the Claude Sonnet 4 model.
