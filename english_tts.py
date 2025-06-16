#!/usr/bin/env python3
"""
영어 학습용 TTS(Text-to-Speech) 프로그램
gTTS 라이브러리를 사용하여 텍스트 파일의 영어 문장들을 MP3 파일로 변환

사용법: python gtts.py <텍스트파일명>
예시: python gtts.py learn_0616.txt
"""

import sys
import os
from gtts import gTTS

def read_text_file(filename):
    """
    텍스트 파일을 읽어서 각 줄을 리스트로 반환
    
    Args:
        filename (str): 읽을 텍스트 파일명
        
    Returns:
        list: 각 줄의 텍스트를 담은 리스트
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return None

def create_combined_audio(sentences, output_filename, lang='en'):
    """
    각 문장을 개별적으로 변환한 후 1초 무음과 함께 결합
    
    Args:
        sentences (list): 변환할 문장들의 리스트
        output_filename (str): 출력할 MP3 파일명
        lang (str): 언어 코드 (기본값: 'en')
    """
    try:
        # ffmpeg 사용 가능 여부 확인
        if not check_ffmpeg_available():
            print("❌ FFmpeg가 설치되어 있지 않습니다.")
            print("   macOS: brew install ffmpeg")
            print("   Ubuntu: sudo apt install ffmpeg")
            print("   Windows: https://ffmpeg.org/download.html")
            return
            
        print("🔧 FFmpeg를 사용하여 고품질 TTS + 오디오 개선을 적용합니다...")
        print("   📊 적용 효과: 볼륨 정규화, 컴프레서, 노이즈 필터링")
        create_audio_with_ffmpeg(sentences, output_filename, lang)
            
    except Exception as e:
        print(f"음성 변환 오류: {e}")
        print("gTTS 라이브러리가 설치되어 있는지 확인해주세요: pip install gtts")

def check_ffmpeg_available():
    """FFmpeg 사용 가능 여부 확인"""
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_audio_with_ffmpeg(sentences, output_filename, lang='en'):
    """FFmpeg를 사용해서 각 문장 사이에 정확히 1초 무음 추가 (고품질 44100Hz, 320kbps)"""
    temp_files = []
    
    try:
        print(f"📝 {len(sentences)}개 문장을 고품질로 개별 변환 중... (44100Hz, 320kbps)")
        
        # 각 문장을 개별 MP3 파일로 생성
        for i, sentence in enumerate(sentences):
            print(f"  🔊 {i+1}/{len(sentences)}: {sentence[:50]}...")
            
            # 개별 TTS 생성 (음질 향상 설정)
            tts = gTTS(text=sentence.strip(), lang='en-us', slow=False)
            
            # 임시 파일에 저장 후 고품질로 변환
            temp_raw_file = f"temp_raw_{i}.mp3"
            temp_file = f"temp_sentence_{i}.mp3"
            
            # 원본 저장
            tts.save(temp_raw_file)
            
            # FFmpeg로 고품질 변환
            convert_to_high_quality(temp_raw_file, temp_file)
            
            temp_files.append(temp_file)
            temp_files.append(temp_raw_file)  # 원본 파일도 정리 목록에 추가
        
        # 1초 무음 파일 생성
        silence_file = "temp_silence.mp3"
        create_silence_mp3(silence_file, duration=1.0)
        temp_files.append(silence_file)
        
        # FFmpeg로 파일들을 결합
        print("🔗 고품질 파일들을 결합하는 중...")
        audio_files = [f"temp_sentence_{i}.mp3" for i in range(len(sentences))]
        combine_files_with_ffmpeg(audio_files, silence_file, output_filename)
        
        print(f"✅ 고품질 음성 파일이 생성되었습니다: {output_filename}")
        print(f"📝 각 문장 사이에 정확히 1초의 무음이 추가되었습니다.")
        print(f"🎵 음질: 44100Hz, 320kbps, 스테레오")
        print(f"🔊 오디오 개선: 볼륨 정규화 + 컴프레서 + 노이즈 필터링")
        
    finally:
        # 임시 파일들 정리
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass

def create_silence_mp3(filename, duration=1.0):
    """지정된 길이의 고품질 무음 MP3 파일 생성"""
    import subprocess
    
    # FFmpeg로 고품질 무음 생성 (44100Hz, 320kbps)
    cmd = [
        'ffmpeg', '-y',  # -y: 덮어쓰기
        '-f', 'lavfi',   # lavfi 입력 형식
        '-i', f'anullsrc=channel_layout=stereo:sample_rate=44100',  # 44100Hz 스테레오 무음
        '-t', str(duration),  # 지속 시간
        '-c:a', 'libmp3lame',   # MP3 인코더
        '-b:a', '320k',  # 320kbps 비트레이트
        '-ar', '44100',  # 44100Hz 샘플링 레이트
        filename
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)

def convert_to_high_quality(input_file, output_file):
    """TTS 파일을 고품질 MP3로 변환 (볼륨 정규화 + 컴프레서 적용)"""
    import subprocess
    
    # FFmpeg로 고품질 변환 + 오디오 개선 필터
    # loudnorm: 볼륨 정규화 (LUFS 표준)
    # acompressor: 다이나믹 레인지 압축으로 음성 명료도 향상
    # highpass: 저주파 노이즈 제거
    # lowpass: 고주파 노이즈 제거 (음성에 불필요한 고주파)
    audio_filters = [
        'highpass=f=80',           # 80Hz 이하 저주파 노이즈 제거
        'lowpass=f=8000',          # 8kHz 이상 고주파 노이즈 제거 (음성 최적화)
        'acompressor=threshold=-18dB:ratio=3:attack=3:release=100:makeup=2dB',  # 컴프레서
        'loudnorm=I=-16:TP=-1.5:LRA=11'  # 볼륨 정규화
    ]
    
    cmd = [
        'ffmpeg', '-y',  # -y: 덮어쓰기
        '-i', input_file,  # 입력 파일
        '-af', ','.join(audio_filters),  # 오디오 필터 체인
        '-c:a', 'libmp3lame',  # MP3 인코더
        '-b:a', '320k',  # 320kbps 비트레이트
        '-ar', '44100',  # 44100Hz 샘플링 레이트
        '-ac', '2',  # 스테레오
        '-q:a', '0',  # 최고 품질
        output_file
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)

def combine_files_with_ffmpeg(audio_files, silence_file, output_filename):
    """FFmpeg를 사용해서 오디오 파일들을 고품질로 무음과 함께 결합 (볼륨 정규화 + 컴프레서)"""
    import subprocess
    
    # FFmpeg 입력 파일 목록 생성
    inputs = []
    filter_parts = []
    
    input_index = 0
    for i, audio_file in enumerate(audio_files):
        inputs.extend(['-i', audio_file])
        filter_parts.append(f'[{input_index}]')
        input_index += 1
        
        # 마지막 파일이 아니면 무음 추가
        if i < len(audio_files) - 1:
            inputs.extend(['-i', silence_file])
            filter_parts.append(f'[{input_index}]')
            input_index += 1
    
    # 파일 결합 + 최종 오디오 개선 필터
    concat_filter = ''.join(filter_parts) + f'concat=n={len(filter_parts)}:v=0:a=1[combined]'
    
    # 최종 오디오 개선 필터 체인
    final_filters = [
        'acompressor=threshold=-16dB:ratio=2.5:attack=5:release=150:makeup=1dB',  # 최종 컴프레션
        'loudnorm=I=-16:TP=-1.5:LRA=11'  # 최종 볼륨 정규화
    ]
    
    # 전체 필터 체인: 결합 → 최종 개선
    full_filter = concat_filter + ';[combined]' + ','.join(final_filters) + '[out]'
    
    # FFmpeg 명령 실행 (고품질 설정 + 오디오 개선)
    cmd = [
        'ffmpeg', '-y'
    ] + inputs + [
        '-filter_complex', full_filter,
        '-map', '[out]',
        '-c:a', 'libmp3lame',  # MP3 인코더
        '-b:a', '320k',  # 320kbps 비트레이트
        '-ar', '44100',  # 44100Hz 샘플링 레이트
        '-ac', '2',  # 스테레오
        '-q:a', '0',  # 최고 품질
        output_filename
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FFmpeg 오류: {result.stderr}")

def main():
    """메인 함수"""
    # 명령행 인자 확인
    if len(sys.argv) != 2:
        print("사용법: python english_tts.py <텍스트파일명>")
        print("예시: python english_tts.py learn_0616.txt")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    
    # 파일 확장자 제거하고 .mp3 확장자로 출력 파일명 생성
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.mp3"
    
    print(f"📖 텍스트 파일 읽는 중: {input_filename}")
    
    # 텍스트 파일 읽기
    sentences = read_text_file(input_filename)
    
    if sentences is None:
        sys.exit(1)
    
    if not sentences:
        print("경고: 파일에 유효한 텍스트가 없습니다.")
        sys.exit(1)
    
    print(f"📝 총 {len(sentences)}개의 문장을 발견했습니다:")
    for i, sentence in enumerate(sentences, 1):
        print(f"  {i}. {sentence}")
    
    print(f"\n🔊 음성 변환 중...")
    
    # 음성 파일 생성
    create_combined_audio(sentences, output_filename)
    
    print(f"\n🎉 완료! '{output_filename}' 파일을 재생해보세요.")

if __name__ == "__main__":
    main()
