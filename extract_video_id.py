


def extract_video_id(url: str) -> str:
    """
    유튜브 URL에서 영상 ID만 추출해서 반환하는 함수야.
    다양한 URL 패턴(youtu.be, youtube.com/watch, /embed/, /v/)을 지원해.

    Args:
        url (str): 유튜브 영상 URL

    Returns:
        str: 영상 ID (없으면 빈 문자열)
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [''])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return ''