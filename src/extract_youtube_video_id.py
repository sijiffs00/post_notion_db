"""
YouTube URL에서 Video ID를 추출하는 모듈

이 모듈은 다양한 형태의 YouTube URL에서 video ID를 추출하는 기능을 제공합니다.
YouTube의 여러 URL 형식을 지원하며, 정규표현식을 사용하여 안전하게 ID를 추출합니다.

지원하는 URL 형식:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID  
- https://www.youtube.com/embed/VIDEO_ID
- https://www.youtube.com/watch?param=value&v=VIDEO_ID&other=value

사용 예시:
    video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # 결과: "dQw4w9WgXcQ"
"""

import re
from typing import Optional


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