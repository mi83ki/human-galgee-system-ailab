import threading

from human_galgee_system.visual_tranceformer import visual_tranceformer
from human_galgee_system.voice_tranceformer import voice_tranceformer

if __name__ == "__main__":
    # 視覚変換のスレッドを開始
    visual_thread = threading.Thread(target=visual_tranceformer.main, daemon=True)
    visual_thread.start()

    try:
        # 音声変換をメインスレッドで実行
        voice_tranceformer.main()
    except KeyboardInterrupt:
        print("finish")
