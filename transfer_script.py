# 스크립트를 뽑을 유튜브영상 id : kDTEvpm5C9Q
# yt-dlp 라이브러리를 사용해서 스크립트를 뽑음.
# 스크립트는 .txt파일로 scripts폴더에 저장

import yt_dlp
import os
import re
from pathlib import Path

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
                    txt_file_path = scripts_dir / f"{video_id}.txt"
                    
                    # 자막 파일을 읽고 정리
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_content = f.read()
                    
                    # VTT 내용을 깔끔한 텍스트로 변환
                    cleaned_text = clean_vtt_content(subtitle_content)
                    
                    # txt 파일로 저장
                    with open(txt_file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_text)
                    
                    # 원본 자막 파일 삭제
                    subtitle_file.unlink()
                    
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
        return {
            'success': False,
            'error': f'다운로드 오류: {str(e)}'
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