from transfer_script import clean_vtt_content

# 테스트용 VTT 내용 (실제 VTT 파일과 유사한 형태)
test_vtt_content = """WEBVTT
Kind: captions
Language: ko

00:00:01.199 --> 00:00:03.389 align:start position:0%
 
얘들아,<00:00:01.520><c> 오늘은</c><00:00:02.159><c> 아예</c><00:00:02.520><c> 각잡고</c><00:00:03.080><c> 남양</c>

00:00:03.389 --> 00:00:03.399 align:start position:0%
얘들아, 오늘은 아예 각잡고 남양
 

00:00:03.399 --> 00:00:05.710 align:start position:0%
얘들아, 오늘은 아예 각잡고 남양
특집이다.<00:00:04.279><c> 오늘도</c><00:00:04.680><c> 이제</c><00:00:04.920><c> 너희들</c><00:00:05.359><c> 사연을</c>

00:00:05.710 --> 00:00:05.720 align:start position:0%
특집이다. 오늘도 이제 너희들 사연을
 

00:00:05.720 --> 00:00:07.590 align:start position:0%
특집이다. 오늘도 이제 너희들 사연을
다<00:00:05.920><c> 이렇게</c><00:00:06.080><c> 받았는데</c><00:00:06.919><c> 너희들은</c><00:00:07.279><c> 사실</c>

00:00:07.590 --> 00:00:07.600 align:start position:0%
다 이렇게 받았는데 너희들은 사실
"""

# 함수 테스트
cleaned_text = clean_vtt_content(test_vtt_content)
print("=== 원본 VTT 내용 ===")
print(test_vtt_content)
print("\n=== 정리된 텍스트 ===")
print(cleaned_text) 