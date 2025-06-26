#!/usr/bin/env python3
"""
English Learning TTS(Text-to-Speech) Program
Convert English sentences from text files to MP3 files using gTTS library

Usage: python english_tts.py <text_filename>
Example: python english_tts.py sample.txt
"""

import sys
import os
import subprocess
from gtts import gTTS
from typing import List, Optional


class TextFileReader:
    """Class responsible for reading and processing text files"""
    
    @staticmethod
    def read_text_file(filename: str) -> Optional[List[str]]:
        """
        Read a text file and return each line as a list
        
        Args:
            filename (str): Name of the text file to read
            
        Returns:
            list: List containing text from each line
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]
            return lines
        except FileNotFoundError:
            print(f"Error: Could not find file '{filename}'.")
            return None
        except Exception as e:
            print(f"File reading error: {e}")
            return None


class AudioProcessor:
    """Class responsible for audio processing and FFmpeg related functionality"""
    
    def __init__(self):
        self.temp_files = []
    
    def check_ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def create_silence_mp3(self, filename: str, duration: float = 2.0) -> None:
        """Generate high-quality silent MP3 file with specified duration"""
        cmd = [
            'ffmpeg', '-y',  # -y: overwrite
            '-f', 'lavfi',   # lavfi input format
            '-i', f'anullsrc=channel_layout=stereo:sample_rate=44100',  # 44100Hz stereo silence
            '-t', str(duration),  # duration
            '-c:a', 'libmp3lame',   # MP3 encoder
            '-b:a', '320k',  # 320kbps bitrate
            '-ar', '44100',  # 44100Hz sampling rate
            filename
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        self.temp_files.append(filename)
    
    def convert_to_high_quality(self, input_file: str, output_file: str) -> None:
        """Convert TTS file to high-quality MP3 (20% volume increase + compressor applied)"""
        # FFmpeg high-quality conversion + audio enhancement filters
        audio_filters = [
            'highpass=f=80',           # Remove low-frequency noise below 80Hz
            'lowpass=f=8000',          # Remove high-frequency noise above 8kHz (voice optimization)
            'acompressor=threshold=-18dB:ratio=3:attack=3:release=100:makeup=2dB',  # Compressor
            'loudnorm=I=-13:TP=-1.0:LRA=11'  # Volume normalization (20% increase, Peak limiting)
        ]
        
        cmd = [
            'ffmpeg', '-y',  # -y: overwrite
            '-i', input_file,  # input file
            '-af', ','.join(audio_filters),  # audio filter chain
            '-c:a', 'libmp3lame',  # MP3 encoder
            '-b:a', '320k',  # 320kbps bitrate
            '-ar', '44100',  # 44100Hz sampling rate
            '-ac', '2',  # stereo
            '-q:a', '0',  # highest quality
            output_file
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        self.temp_files.append(output_file)
    
    def combine_files_with_ffmpeg(self, audio_files: List[str], silence_file: str, output_filename: str) -> None:
        """Combine audio files with silence using FFmpeg in high quality"""
        # Generate FFmpeg input file list
        inputs = []
        filter_parts = []
        
        input_index = 0
        for i, audio_file in enumerate(audio_files):
            inputs.extend(['-i', audio_file])
            filter_parts.append(f'[{input_index}]')
            input_index += 1
            
            # Add silence after all files (including the last one)
            inputs.extend(['-i', silence_file])
            filter_parts.append(f'[{input_index}]')
            input_index += 1
        
        # File combination + final audio enhancement filters
        concat_filter = ''.join(filter_parts) + f'concat=n={len(filter_parts)}:v=0:a=1[combined]'
        
        # Final audio enhancement filter chain
        final_filters = [
            'acompressor=threshold=-16dB:ratio=2.5:attack=5:release=150:makeup=1dB',  # Final compression
            'loudnorm=I=-13:TP=-1.0:LRA=11'  # Final volume normalization (20% increase, Peak limiting)
        ]
        
        # Complete filter chain: combination → final enhancement
        full_filter = concat_filter + ';[combined]' + ','.join(final_filters) + '[out]'
        
        # Execute FFmpeg command (high-quality settings + audio enhancement)
        cmd = [
            'ffmpeg', '-y'
        ] + inputs + [
            '-filter_complex', full_filter,
            '-map', '[out]',
            '-c:a', 'libmp3lame',  # MP3 encoder
            '-b:a', '320k',  # 320kbps bitrate
            '-ar', '44100',  # 44100Hz sampling rate
            '-ac', '2',  # stereo
            '-q:a', '0',  # highest quality
            output_filename
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")
    
    def cleanup_temp_files(self) -> None:
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        self.temp_files.clear()


class TTSConverter:
    """Main class responsible for TTS conversion"""
    
    def __init__(self, lang: str = 'en-us'):
        self.lang = lang
        self.audio_processor = AudioProcessor()
    
    def create_combined_audio(self, sentences: List[str], output_filename: str) -> None:
        """
        Convert each sentence individually then combine with 2-second silence
        
        Args:
            sentences (list): List of sentences to convert
            output_filename (str): Output MP3 filename
        """
        try:
            # Check if ffmpeg is available
            if not self.audio_processor.check_ffmpeg_available():
                print("❌ FFmpeg is not installed.")
                print("   macOS: brew install ffmpeg")
                print("   Ubuntu: sudo apt install ffmpeg")
                print("   Windows: https://ffmpeg.org/download.html")
                return
                
            print("🔧 Using FFmpeg for high-quality TTS + audio enhancement...")
            print("   📊 Applied effects: 20% volume increase, compressor, noise filtering")
            self._create_audio_with_ffmpeg(sentences, output_filename)
                
        except Exception as e:
            print(f"Voice conversion error: {e}")
            print("Please check if gTTS library is installed: pip install gtts")
    
    def _create_audio_with_ffmpeg(self, sentences: List[str], output_filename: str) -> None:
        """Use FFmpeg to add exactly 2 seconds of silence between each sentence (high-quality 44100Hz, 320kbps)"""
        try:
            print(f"📝 Converting {len(sentences)} sentences individually to high quality... (44100Hz, 320kbps)")
            
            # Generate each sentence as individual MP3 file
            for i, sentence in enumerate(sentences):
                print(f"  🔊 {i+1}/{len(sentences)}: {sentence[:50]}...")
                
                # Generate individual TTS (US English)
                tts = gTTS(text=sentence.strip(), lang=self.lang, slow=False)
                
                # Save to temporary file then convert to high quality
                temp_raw_file = f"temp_raw_{i}.mp3"
                temp_file = f"temp_sentence_{i}.mp3"
                
                # Save original
                tts.save(temp_raw_file)
                
                # Convert to high quality with FFmpeg
                self.audio_processor.convert_to_high_quality(temp_raw_file, temp_file)
                
                self.audio_processor.temp_files.append(temp_raw_file)
            
            # Generate 2-second silence file
            silence_file = "temp_silence.mp3"
            self.audio_processor.create_silence_mp3(silence_file, duration=2.0)
            
            # Combine files with FFmpeg
            print("🔗 Combining high-quality files...")
            audio_files = [f"temp_sentence_{i}.mp3" for i in range(len(sentences))]
            self.audio_processor.combine_files_with_ffmpeg(audio_files, silence_file, output_filename)
            
            print(f"✅ High-quality audio file has been created: {output_filename}")
            print(f"📝 Exactly 2 seconds of silence has been added between each sentence and at the end.")
            print(f"🎵 Audio quality: 44100Hz, 320kbps, stereo")
            print(f"🔊 Audio enhancement: 20% volume increase + compressor + noise filtering")
            
        finally:
            # Clean up temporary files
            self.audio_processor.cleanup_temp_files()


class EnglishTTSApp:
    """Main class for the English TTS application"""
    
    def __init__(self, lang: str = 'en-us'):
        self.text_reader = TextFileReader()
        self.tts_converter = TTSConverter(lang)
    
    def process_file(self, input_filename: str) -> None:
        """Process text file and convert to audio file"""
        # Remove file extension and generate output filename with .mp3 extension
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}.mp3"
        
        print(f"📖 Reading text file: {input_filename}")
        
        # Read text file
        sentences = self.text_reader.read_text_file(input_filename)
        
        if sentences is None:
            return
        
        if not sentences:
            print("Warning: No valid text found in file.")
            return
        
        print(f"📝 Found a total of {len(sentences)} sentences:")
        for i, sentence in enumerate(sentences, 1):
            print(f"  {i}. {sentence}")
        
        print(f"\n🔊 Converting to audio...")
        
        # Generate audio file
        self.tts_converter.create_combined_audio(sentences, output_filename)
        
        print(f"\n🎉 Complete! Please play '{output_filename}' file.")
    
    def run(self, args: List[str]) -> None:
        """Run the application"""
        # Check command line arguments
        if len(args) != 2:
            print("Usage: python english_tts.py <text_filename>")
            print("Example: python english_tts.py sample.txt")
            return
        
        input_filename = args[1]
        self.process_file(input_filename)


def main():
    """Main function"""
    app = EnglishTTSApp()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
