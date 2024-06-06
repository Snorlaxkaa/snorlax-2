from gtts import gTTS
import playsound
import tempfile
import time
from pydub import AudioSegment  # 導入pydub處理音頻

def speak_and_print(text, lang='zh-tw', wait=False):
    print(text)
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            
            # 使用pydub加载音频文件并获取时长
            audio = AudioSegment.from_file(fp.name)
            duration = len(audio) / 1000.0  
            
            playsound.playsound(fp.name)
            
            # 移除以下行如果 playsound 正確同步
            # if wait:
            #     time.sleep(duration)  # 使用音頻的實際時長進行等待
    except Exception as e:
        print(f"发生错误: {e}")


