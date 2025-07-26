# 유튜브영상id를 제공하면 스크립트를 뽑아서 scripts폴더에 저장

import yt_dlp
import os
import re
from pathlib import Path

# youtube-transcript-api 대체 방법
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_AVAILABLE = False

def clean_vtt_content(vtt_content: str) -> str:
    """
    VTT 파일 내용을 깔끔한 텍스트로 변환
    
    Args:
        vtt_content (str): VTT 파일의 원본 내용
        
    Returns:
        str: 정리된 텍스트
    """
    lines = vtt_content.split('\n')
    cleaned_lines = []
    seen_texts = set()  # 중복 제거를 위한 set
    
    for line in lines:
        # 타임스탬프 라인 건너뛰기
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue
        # 빈 줄 건너뛰기
        if line.strip() == '':
            continue
        # WEBVTT 헤더 건너뛰기
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        # align:start position:0% 같은 텍스트 제거
        if 'align:start position:' in line:
            continue
            
        # HTML 태그 제거
        line = re.sub(r'<[^>]+>', '', line)
        # 특수 문자 제거 (타임스탬프 관련)
        line = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}', '', line)
        
        # 정리된 텍스트
        cleaned_line = line.strip()
        
        # 중복 제거: 같은 텍스트가 이미 있으면 건너뛰기
        if cleaned_line and cleaned_line not in seen_texts:
            seen_texts.add(cleaned_line)
            cleaned_lines.append(cleaned_line)
    
    return '\n'.join(cleaned_lines)

def extract_script_with_transcript_api(video_id: str, scripts_dir: Path) -> dict:
    """
    youtube-transcript-api를 사용해서 자막 추출
    
    Args:
        video_id (str): 유튜브 영상 ID
        scripts_dir (Path): 스크립트 저장 디렉토리
        
    Returns:
        dict: 결과 딕셔너리
    """
    try:
        # YouTubeTranscriptApi 인스턴스 생성
        ytt_api = YouTubeTranscriptApi()
        
        # 한국어 자막 우선 시도
        try:
            transcript_data = ytt_api.fetch(video_id, languages=['ko'])
            print("한국어 자막 사용")
        except:
            # 한국어가 없으면 영어 시도
            try:
                transcript_data = ytt_api.fetch(video_id, languages=['en'])
                print("영어 자막 사용")
            except:
                # 영어도 없으면 자동 생성 자막 시도
                transcript_data = ytt_api.fetch(video_id)
                print("자동 생성 자막 사용")
        
        # 텍스트 추출
        text_lines = []
        for item in transcript_data:
            text_lines.append(item.text)
        
        # 텍스트 합치기
        full_text = '\n'.join(text_lines)
        
        # 파일 저장
        txt_file_path = scripts_dir / "video_script.txt"
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        return {
            'success': True,
            'file_path': str(txt_file_path),
            'message': f'스크립트가 성공적으로 저장되었습니다: {txt_file_path} (youtube-transcript-api 사용)'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'youtube-transcript-api 오류: {str(e)}'
        }

def transfer_script(video_id: str) -> dict:
    """
    유튜브 영상 ID로 스크립트를 추출하여 scripts 폴더에 .txt 파일로 저장
    
    Args:
        video_id (str): 유튜브 영상 ID
        
    Returns:
        dict: {
            'success': bool,
            'file_path': str (성공시 파일 경로),
            'error': str (실패시 에러 메시지)
        }
    """
    try:
        # scripts 폴더 생성 (없으면)
        scripts_dir = Path("scripts")
        scripts_dir.mkdir(exist_ok=True)
        
        # 유튜브 URL 생성
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # yt-dlp 옵션 설정
        ydl_opts = {
            'writesubtitles': True,        # 수동 자막 다운로드
            'writeautomaticsub': True,     # 자동 자막 다운로드
            'subtitleslangs': ['ko', 'en'], # 한국어, 영어 자막 우선
            'skip_download': True,         # 영상 다운로드 안함
            'outtmpl': str(scripts_dir / f'{video_id}.%(ext)s'),  # 출력 파일명
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
            },
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'quiet': False,
            'sleep_interval': 3,  # 요청 간 3초 대기
            'max_sleep_interval': 10,  # 최대 10초 대기
            'retries': 3,  # 재시도 횟수
            'fragment_retries': 3,
            'extractor_retries': 3,
            'file_access_retries': 3,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'live'],  # DASH와 라이브 스트림 건너뛰기
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 영상 정보 추출
            info = ydl.extract_info(url, download=False)
            
            # 자막 정보 확인
            if 'subtitles' in info or 'automatic_captions' in info:
                # 자막 다운로드 실행
                ydl.download([url])
                
                # 다운로드된 자막 파일 찾기
                subtitle_files = list(scripts_dir.glob(f"{video_id}.*"))
                
                if subtitle_files:
                    # 첫 번째 자막 파일을 txt로 변환
                    subtitle_file = subtitle_files[0]
                    
                    # 자막 파일을 읽고 정리
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_content = f.read()
                    
                    # VTT 내용을 깔끔한 텍스트로 변환
                    cleaned_text = clean_vtt_content(subtitle_content)
                    
                    # txt 파일로 저장
                    txt_file_path = scripts_dir / "video_script.txt"
                    with open(txt_file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_text)
                    
                    # 모든 VTT 파일 삭제
                    for vtt_file in subtitle_files:
                        vtt_file.unlink()
                    
                    return {
                        'success': True,
                        'file_path': str(txt_file_path),
                        'message': f'스크립트가 성공적으로 저장되었습니다: {txt_file_path}'
                    }
                else:
                    return {
                        'success': False,
                        'error': '자막 파일을 찾을 수 없습니다.'
                    }
            else:
                return {
                    'success': False,
                    'error': '이 영상에는 자막이 없습니다.'
                }
                
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"yt-dlp 오류: {error_msg}")
        if "Sign in to confirm you're not a bot" in error_msg or "HTTP Error 429" in error_msg:
            # yt-dlp가 봇 감지나 요청 제한으로 실패하면 youtube-transcript-api 시도
            if YOUTUBE_TRANSCRIPT_AVAILABLE:
                print("yt-dlp 실패, youtube-transcript-api로 재시도...")
                # scripts_dir이 정의되지 않았을 수 있으므로 다시 생성
                scripts_dir = Path("scripts")
                scripts_dir.mkdir(exist_ok=True)
                return extract_script_with_transcript_api(video_id, scripts_dir)
            else:
                return {
                    'success': False,
                    'error': 'YouTube에서 접근 제한. 잠시 후 다시 시도해주세요.'
                }
        else:
            return {
                'success': False,
                'error': f'다운로드 오류: {error_msg}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'예상치 못한 오류: {str(e)}'
        }

# 테스트용 코드
if __name__ == "__main__":
    video_id = "kDTEvpm5C9Q"
    result = transfer_script(video_id)
    print(result)