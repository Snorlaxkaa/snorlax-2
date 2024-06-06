import sys
import re
import time
from gtts import gTTS  # 文本转语音库
import playsound  # 用于播放音频文件
from pynput import keyboard
import speech_recognition as sr  # 语音数据转换为文本
import jieba  # 使用jieba进行分词
from models.index import connect_to_database, get_student  # 数据库
from Snorlax.spack import speak_and_print  # 语音合成

# 初始化数据库连接和用户字典
connection = connect_to_database()
users_dict = get_student(connection) if connection else {}

# 全局变量用于控制录音状态
recording = False
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_and_recognize(retry=False):
    """监听并识别用户的语音输入，返回识别的文本"""
    global recognizer, mic
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("请说话...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language='zh-TW')
        print("识别结果:", text)
        return text
    except sr.UnknownValueError:
        if not retry:
            speak_and_print("抱歉，我没有听清楚，请再说一次", wait=True)
            return listen_and_recognize(retry=True)
        else:
            speak_and_print("再次识别失败，请稍后再试。", wait=True)
            return ""
    except sr.RequestError as e:
        speak_and_print(f"无法从Google Speech Recognition服务获取结果; {e}", wait=True)
        return ""

def chinese_number(cn_number):
    """将中文数字转换为阿拉伯数字"""
    chinese_to_arabic = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
    return ''.join(chinese_to_arabic.get(char, char) for char in cn_number)

def on_press(key):
    """键盘按下事件处理函数"""
    global recording, recognizer, mic

    try:
        # 检测是否按下 'q' 键
        if key.char == 'q':  # 使用 .char 来获取按键的字符表示 
            print("退出程序...")
            sys.exit(0)  # 安全退出程序
    except AttributeError:
        # 某些键（如特殊键）没有字符表示，这里忽略这种情况
        pass

    if key == keyboard.Key.space:  # 如果按下的是空格键
        if not recording:
            recording = True  # 更新录音状态为开始录音
            print("开始录音...")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)  # 调整麦克风收集噪音
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='zh-TW')  # 使用Google的API进行语音识别
                print("识别结果:", text)
            except sr.UnknownValueError:
                print("Google Speech Recognition 无法理解音频")
            except sr.RequestError as e:
                print(f"无法从Google Speech Recognition服务获取结果; {e}")
            recording = False  # 更新录音状态为停止录音
            print("录音已停止.")
        else:
            print("正在录音中，请停止后重新按键开始新的录音。")

def handle_input(text):
    """处理用户的语音输入"""
    text = chinese_number(text)  # 转换中文数字
    user_id_match = re.search(r'\d+', text)
    question_keywords = ['请问', '怎么', '什么', '为什么', '我要']

    if user_id_match:
        user_id = user_id_match.group()
        if user_id in users_dict:
            user_name = users_dict[user_id]
            speak_and_print(f"你好, {user_name}，欢迎光临。你今天要来做什么？", wait=True)
            chat_with_user(user_name)
        else:
            speak_and_print("抱歉，我找不到您的ID。您想要再说一次，还是退出程序？", wait=True)
            handle_user_decision()
    elif any(keyword in text for keyword in question_keywords):
        chat_with_user("陌生人")

def chat_with_user(user_name):
    """回答问题"""
    speak_and_print(f"你好, {user_name}。请问您需要什么帮助？", wait=True)
    while True:
        user_response = listen_and_recognize()  # 获取用户回应
        if user_response.lower() in ["再见", "退出"]:
            speak_and_print("好的，再见！", wait=True)
            break
        response_keywords = cut_words(user_response)
        process_query(response_keywords, user_name)

def cut_words(sentence, mode='default'):
    """使用jieba进行分词"""
    if mode == 'full':
        return list(jieba.cut(sentence, cut_all=True))
    elif mode == 'search':
        return list(jieba.cut_for_search(sentence))
    else:
        return list(jieba.cut(sentence))

def process_query(keywords, user_name):
    if "开门" in keywords:
        speak_and_print("好的，门已解锁。", wait=True)
    elif "幾點" in keywords:
        time_response = get_time()
        speak_and_print(time_response, wait=True)
    else:
        speak_and_print("不好意思，我无法回答你的问题。可以问我其他问题吗？", wait=True)

def get_time():
    """获取当前时间"""
    current_time = time.strftime('%Y年%m月%d日 %H点%M分')
    return f"现在时间是{current_time}"

def handle_user_decision():
    """退出或重新开始程序"""
    user_choice = listen_and_recognize()
    if "确定" in user_choice:
        sys.exit()  # 退出程序

def main():
    """主函数，设置键盘监听"""
    speak_and_print("你好我是虚拟助手，请按空格键开始说话", wait=True)
    listener.join()

if __name__ == "__main__":
    main()
 