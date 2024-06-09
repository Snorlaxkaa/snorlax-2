import sys
from gtts import gTTS # 文本轉語音函式庫 
from anyio import run 
from pynput import keyboard
import speech_recognition as sr
import os   
import re   #
import playsound  # 用於播放音頻文件
from pynput import keyboard
from pprint import pprint  # 導入pprint函數
import threading    # 於創建一個新的線程來異步執行語音播放操作
import jieba
import logging
import sys
from pynput import keyboard
import tempfile # 用於生成臨時文件和目錄
import time
import speech_recognition as sr # 語音數據轉換為文本
from models.index import connect_to_database, get_student   #資料庫
from Snorlax.spack import speak_and_print # 語音合成
from Snorlax.Weather import get_weather # 天氣API
from Snorlax.tcp_server import user_face, start_server # TCP伺服器
connection = connect_to_database()
users_dict = get_student(connection) if connection else {}


def listen_and_recognize(retry=False):
    """監聽並識別用戶的語音輸入，返回識別的文本"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("請說話...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='zh-TW')
        print("識別結果:", text)  # 印出識別結果ㄉ
        return text
    except sr.UnknownValueError:
        if not retry:
            speak_and_print("抱歉，我沒有聽清楚，請再說一次", wait=True)
            return listen_and_recognize(retry=True)
        else:
            speak_and_print("再次識別失敗，請稍後再試。", wait=True)
            sys.exit()  # 退出程式
    except sr.RequestError as e:
        speak_and_print(f"無法從Google Speech Recognition服務獲取結果; {e}", wait=True)
    return ""

def chinese_number(cn_number):
    """將中文數字轉換為阿拉伯數字"""
    chinese_to_arabic = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
    return ''.join(chinese_to_arabic.get(char, char) for char in cn_number)

def u_input_(input_text):
    """處理使用者輸入"""
    input_text = chinese_number(input_text) # 轉換中文數字
    user_id_match = re.search(r'\d+', input_text)
    user_id = user_id_match.group() if user_id_match else None
    
    if user_id and user_id in users_dict:
        user_name = users_dict[user_id]
        speak_and_print(f"你好, {user_name}，歡迎光臨。你今天要來做什麼？", wait=True)
        chat_with_user(user_name)
    else:
        speak_and_print("抱歉，我找不到您的ID。您有其他問題嗎？", wait=True)



def cut_words(sentence, mode='default'):
    """
    使用jieba進行分詞。
    :param sentence: 待分詞的句子。
    :param mode: 分詞模式，'default'為默認精確模式，'full'為全模式，'search'為搜索引擎模式。
    :return: 分詞結果的列表。
    """
    if mode == 'full':
        return list(jieba.cut(sentence, cut_all=True))
    elif mode == 'search':
        return list(jieba.cut_for_search(sentence))
    else:
        return list(jieba.cut(sentence))


def chat_with_user(user_name):
    """回答問題"""
    while True:
        user_response = listen_and_recognize()  # 獲取用戶回應
        response_keywords = cut_words(user_response)
        if "開門" in response_keywords:
            speak_and_print("好的，門已解鎖。", wait=True)
            main()
            break
        elif "幾點" in response_keywords:
            time_response = get_time()
            speak_and_print(time_response, wait=True)
            speak_and_print(f"{user_name}, 還有其他問題嗎？", wait=True)
            if "沒有" in response_keywords:
                    speak_and_print("好的，如果您有其他問題，請隨時告訴我。", wait=True)
                    break
        elif "找人" in response_keywords:
            find_person()
            speak_and_print("還有其他問題嗎？", wait=True)
        elif "老師" in response_keywords:
            Director(user_name)
            speak_and_print("還有其他問題嗎？", wait=True)
        elif "天氣" in response_keywords:
            temperature = get_weather("永康區")
            speak_and_print(f"今 天的溫度是{temperature}度。", wait=True)
        else:
            speak_and_print("不好意思，我無法回答你的問題，可以問我其他問題嗎？還是你要退出？", wait=True)
            handle_user_decision()
        # 根據用戶回答決定是否繼續對話或退出
        if "沒有" in response_keywords:
            speak_and_print("好的，再見！", wait=True)
            break


    

def question():
    speak_and_print("你有什麼問題嗎？", wait=True)

def get_time():
    """獲取當前時間"""
    current_time = time.strftime('%Y年%m月%d日 %H點%M分')
    return f"現在時間是{current_time}"

def members():
    """回答實驗室成員"""
    speak_and_print("我們實驗室的有：", wait=True)
    for(user_id, user_name) in users_dict.items():
        speak_and_print(f"用戶ID: {user_id}, 用戶名: {user_name}", wait=True)
    #這裡要的話要再從資料庫中取出成員名單
    

def Director(user_name):
    """回答實驗室老師"""
    speak_and_print("我們實驗室的主任是鄞宗賢", wait=True)
    speak_and_print(f"{user_name}, 你想知道他的更多資訊嗎？", wait=True)
    user_Director = listen_and_recognize()
    if "不用" in user_Director:
            chat_with_user(user_name)

def find_person():
    """回答找人"""
    connection = connect_to_database()
    users_dict = get_student(connection)
    for user_id, user_name in users_dict.items():
        print(f"用戶ID: {user_id}, 用戶名: {user_name}")

    speak_and_print("你想找誰呢？", wait=True)
    user_find_person = listen_and_recognize()

def handle_user_decision():
    """退出或重新開始程式"""
    user_choice = listen_and_recognize()
    if "再說一次" in user_choice:
        main()
    elif "退出" in user_choice:
        speak_and_print("請問您確定要退出程式嗎？", wait=True)
        user_choice = listen_and_recognize()  # 等待使用者回答
        if "確定" in user_choice:
            speak_and_print("好的，感謝您的使用，再見！", wait=True)
            sys.exit()  # 退出程式
     

def main():
    speak_and_print("你好我是虛擬助手，請說出您的ID或是你的問題", wait=True)
    user_input = listen_and_recognize()
    user_input = chinese_number(user_input)  # 轉換中文數字

    # 使用正則表達式來檢測是否包含數字，假設ID只包含數字
    user_id_match = re.search(r'\d+', user_input)
    # 檢測是否為問題
    question_keywords = ['請問', '怎麼', '什麼', '為什麼', '我要']

    if user_id_match:
        user_id = user_id_match.group()
        if user_id in users_dict:
            user_name = users_dict[user_id]
            speak_and_print(f"你好, {user_name}，歡迎光臨。你今天要來做什麼？", wait=True)
            chat_with_user(user_name)  
        else:
            speak_and_print("抱歉，我找不到您的ID。您想要再說一次，還是退出程式？", wait=True)
            handle_user_decision()
    elif any(keyword in user_input for keyword in question_keywords):
        user_name = "訪客"
        chat_with_user(user_name)  
      
  
if __name__ == "__main__":
        main()
        start_server()
