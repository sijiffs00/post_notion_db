def get_youtube_script(youtube_url: str) -> str:
    """
    주어진 유튜브 URL에서 영상의 스크립트(자막)를 추출해서 반환하는 함수야.
    실제 구현에서는 youtube_transcript_api 같은 라이브러리를 사용할 수 있어.
    
    Args:
        youtube_url (str): 스크립트를 추출할 유튜브 영상의 URL

    Returns:
        str: 추출된 스크립트(자막) 텍스트. 자막이 없으면 빈 문자열 반환.
    """
    # TODO: 실제로는 youtube_transcript_api.get_transcript 등으로 자막을 받아와야 해
    # 여기서는 예시로만 동작하게 임시 문자열을 반환할게
    # 실제 구현 시에는 예외 처리(자막 없는 경우 등)도 추가해야 해
    
    # 예시 반환값
    return "이곳에 유튜브 영상의 스크립트가 들어갈 거야." 