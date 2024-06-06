import speech_recognition as sr # 語音數據轉換為文本
from main import speak_and_print

def listen_and_recognize(retry=False):
    """監聽並識別用戶的語音輸入，返回識別的文本"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("請說話...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='zh-TW')
        return text
    except sr.UnknownValueError:
        if not retry:
            speak_and_print("抱歉，我沒有聽清楚，請再說一次", wait=True)
            return listen_and_recognize(retry=True)
        else:
            speak_and_print("再次識別失敗，請稍後再試。", wait=True)
    except sr.RequestError as e:
        speak_and_print(f"無法從Google Speech Recognition服務獲取結果; {e}", wait=True)
    return ""

def chinese_number(cn_number):
    """將中文數字轉換為阿拉伯數字"""
    chinese_to_arabic = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
    return ''.join(chinese_to_arabic.get(char, char) for char in cn_number)
