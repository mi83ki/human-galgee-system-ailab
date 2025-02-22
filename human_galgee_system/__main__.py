import threading
import time

from human_galgee_system.visual_tranceformer import visual_tranceformer
from human_galgee_system.voice_tranceformer import voice_tranceformer

ENABLE_VISUAL_TRANSFORMATION = True
ENABLE_VOICE_TRANSFORMATION = True

if __name__ == "__main__":
    # 視覚変換のスレッドを開始
    if ENABLE_VISUAL_TRANSFORMATION:
        visual_thread = threading.Thread(target=visual_tranceformer.main, daemon=True)
        visual_thread.start()

    try:
        if ENABLE_VOICE_TRANSFORMATION:
            # 音声変換をメインスレッドで実行
            voice_tranceformer.main()
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("finish")
