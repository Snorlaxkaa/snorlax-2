from gtts import gTTS
import playsound
import os
from pydub import AudioSegment  # 導入pydub處理音頻

def speak_and_print(text, lang='zh-tw', wait=False):
    print(text)
    try:
        # 指定一個你有寫入權限的目錄
        output_dir = os.path.dirname(os.path.abspath(__file__))  # 當前程式所在的目錄
        output_path = os.path.join(output_dir, "output.mp3")  # 生成的 MP3 檔案名稱
        
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        
        # 使用pydub加载音频文件并获取时长
        audio = AudioSegment.from_file(output_path)
        duration = len(audio) / 1000.0
        
        
        playsound.playsound(output_path.replace("\\", "/"))      
          
        # 移除以下行如果 playsound 正確同步
        #if wait:
           # time.sleep(duration)  # 使用音頻的實際時長進行等待
    except Exception as e:
        print(f"发生错误: {e}")


