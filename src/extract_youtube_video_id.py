import re
from typing import Optional

# 유튜브영상url을 제공하면 영상id값만 추출해서 뱉음
def extract_video_id(url: str) -> Optional[str]:

    try:
        # YouTube URL 패턴들 - 다양한 형식을 지원
        patterns = [
            # youtube.com/watch?v= 형식
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            # youtube.com/watch?param=value&v= 형식 (다른 파라미터가 있는 경우)
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        # 각 패턴을 순서대로 시도
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # video ID가 유효한지 간단한 검증 (11자리 영숫자)
                if len(video_id) == 11 and video_id.isalnum():
                    return video_id
        
        return None
        
    except Exception as e:
        print(f"Video ID 추출 중 에러 발생: {e}")
        return None


def validate_youtube_url(url: str) -> bool:
    """
    URL이 유효한 YouTube URL인지 검증하는 함수
    
    Args:
        url (str): 검증할 URL
        
    Returns:
        bool: 유효한 YouTube URL이면 True, 아니면 False
        
    Examples:
        >>> validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        True
        >>> validate_youtube_url("https://example.com")
        False
    """
    return extract_video_id(url) is not None


# 테스트 코드 (모듈을 직접 실행할 때만 실행)
if __name__ == "__main__":
    # 테스트 케이스들
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?param=value&v=dQw4w9WgXcQ&other=value",
        "https://example.com",
        "https://www.youtube.com/watch",
        ""
    ]
    
    print("YouTube Video ID 추출 테스트")
    print("=" * 50)
    
    for url in test_urls:
        video_id = extract_video_id(url)
        status = "✅ 성공" if video_id else "❌ 실패"
        print(f"URL: {url}")
        print(f"결과: {video_id} ({status})")
        print("-" * 30) 