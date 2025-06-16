# 영어 학습용 고품질 TTS 프로그램

gTTS(Google Text-to-Speech)와 FFmpeg를 사용하여 텍스트 파일의 영어 문장들을 고품질 MP3 파일로 변환하는 프로그램입니다.

## 특징

- ✅ **고품질 음성**: 44100Hz, 320kbps, 스테레오
- ✅ **정확한 1초 pause**: 각 문장 사이에 정확히 1초 무음 추가
- ✅ **오디오 개선**: 볼륨 정규화 + 컴프레서 + 노이즈 필터링
- ✅ **미국식 영어**: en-us 발음으로 더 정확한 발음
- ✅ **명료한 음성**: 작은 자음도 선명하게 들림

## 필요 조건

### 1. Python 라이브러리
```bash
pip install gtts
```

### 2. FFmpeg 설치 (필수)

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
1. [FFmpeg 공식 사이트](https://ffmpeg.org/download.html)에서 다운로드
2. 압축 해제 후 PATH에 추가

**설치 확인:**
```bash
ffmpeg -version
```

## 사용법

```bash
python english_tts.py <텍스트파일명>
```

### 예시

```bash
python english_tts.py learn_0616.txt
```

위 명령을 실행하면 `learn_0616.mp3` 파일이 생성됩니다.

## 처리 과정

1. **개별 TTS 변환**: 각 문장을 미국식 영어로 개별 변환
2. **고품질 처리**: FFmpeg로 44100Hz, 320kbps 변환
3. **오디오 개선**: 노이즈 제거, 볼륨 정규화, 컴프레서 적용
4. **1초 무음 삽입**: 정확한 타이밍으로 문장 사이 pause 추가
5. **최종 결합**: 모든 요소를 고품질로 결합

## 파일 구조

- `english_tts.py`: 메인 프로그램
- `learn_0616.txt`: 예시 영어 문장 파일
- `requirements.txt`: 필요한 Python 패키지 목록
- `README.md`: 사용법 안내

## 오디오 품질 개선 사항

### 🎵 음질 향상
- **샘플링 레이트**: 44100Hz (CD 품질)
- **비트레이트**: 320kbps (최고 MP3 품질)
- **채널**: 스테레오

### 🔊 오디오 처리
- **볼륨 정규화**: LUFS 표준으로 일정한 음량 유지
- **다이나믹 컴프레서**: 작은 소리는 크게, 큰 소리는 적당히
- **노이즈 필터링**: 80Hz~8kHz 음성 주파수 대역에 집중

### ⏱️ 타이밍
- **정확한 1초 pause**: 텍스트 기반이 아닌 실제 무음 삽입
- **자연스러운 전환**: 문장 간 부드러운 연결

## 텍스트 파일 형식

텍스트 파일은 다음과 같은 형식으로 작성하세요:
- 한 줄에 하나의 영어 문장
- 빈 줄은 자동으로 무시됩니다
- UTF-8 인코딩으로 저장

### 예시 (learn_0616.txt):
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

## 출력 예시

프로그램 실행 시 다음과 같은 정보가 표시됩니다:

```
📖 텍스트 파일 읽는 중: learn_0616.txt
📝 총 8개의 문장을 발견했습니다:
  1. Hello, how are you today?
  2. I am learning English with Python.
  ...

🔧 FFmpeg를 사용하여 고품질 TTS + 오디오 개선을 적용합니다...
   📊 적용 효과: 볼륨 정규화, 컴프레서, 노이즈 필터링

📝 8개 문장을 고품질로 개별 변환 중... (44100Hz, 320kbps)
  🔊 1/8: Hello, how are you today?...
  🔊 2/8: I am learning English with Python...
  ...

🔗 고품질 파일들을 결합하는 중...
✅ 고품질 음성 파일이 생성되었습니다: learn_0616.mp3
📝 각 문장 사이에 정확히 1초의 무음이 추가되었습니다.
🎵 음질: 44100Hz, 320kbps, 스테레오
🔊 오디오 개선: 볼륨 정규화 + 컴프레서 + 노이즈 필터링

🎉 완료! 'learn_0616.mp3' 파일을 재생해보세요.
```

## 트러블슈팅

### FFmpeg 관련 오류
프로그램이 FFmpeg를 찾을 수 없다는 오류가 발생하면:

1. **FFmpeg 설치 확인**:
   ```bash
   ffmpeg -version
   ```

2. **macOS에서 설치**:
   ```bash
   brew install ffmpeg
   ```

3. **Ubuntu/Debian에서 설치**:
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

### 인터넷 연결 필요
- gTTS는 Google의 온라인 TTS 서비스를 사용합니다
- 변환 시 인터넷 연결이 필요합니다

### 긴 텍스트 처리
- 각 문장이 개별적으로 처리되므로 많은 문장이 있으면 시간이 걸릴 수 있습니다
- 진행 상황이 실시간으로 표시됩니다

## 영어 학습 활용법

### 🎧 듣기 연습
- 각 문장 사이 1초 pause로 명확한 구분
- 고품질 음성으로 정확한 발음 학습

### 🗣️ 따라하기 연습  
- 문장 사이 pause를 활용해 따라 말하기
- 컴프레서로 모든 소리가 명확하게 들림

### 📝 받아쓰기 연습
- 볼륨 정규화로 일정한 음량
- 노이즈 필터링으로 깨끗한 음성

## 참고사항

- 인터넷 연결이 필요합니다 (Google TTS API 사용)
- 생성된 MP3 파일은 미국식 영어 발음으로 재생됩니다
- 최고 품질 설정으로 파일 크기가 클 수 있습니다

## 개발 정보

이 프로그램은 Claude Sonnet 4 모델을 통해 GitHub Copilot Agent mode로 작성되었습니다.
