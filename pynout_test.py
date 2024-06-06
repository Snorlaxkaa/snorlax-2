import sys
from pynput import keyboard
import speech_recognition as sr

recording = False  # 初始状态，未开始录音
recognizer = sr.Recognizer()
mic = sr.Microphone()

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

def main():
    """主函数，设置键盘监听"""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # 等待监听器结束

if __name__ == "__main__":
    main()
 