#!/usr/bin/env python
import argparse
import copy
import threading
import time
from pathlib import Path

import cv2 as cv
import mediapipe as mp
import webuiapi
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from human_galgee_system.utils import CvFpsCalc

IMAGE_DIR = "data/images/temp/"
FACETRIM_IMAGE_PATH = f"{IMAGE_DIR}facetrim.png"
CONVERTED_IMAGE_PATH = f"{IMAGE_DIR}girlimage.png"

# 画像が更新されたかのフラグ
g_is_image_updated = True
g_olimage = None
g_lock = threading.Lock()

# StableDiffusionのimg2imgで画像を生成する
def conv_face2girl(api, prompt, faceimage):
    global g_is_image_updated
    # 画像を生成する
    # faceimage = Image.open(FACETRIM_IMAGE_PATH)
    print({"prompt": prompt})
    try:
        girlimage = api.img2img(
            images=[faceimage],
            prompt=prompt,
            seed=5555,
            cfg_scale=6.5,
            denoising_strength=0.5,
        )
        girlimage.image.save(CONVERTED_IMAGE_PATH)
        with g_lock:
            g_is_image_updated = True
    except Exception as ex:
        print({"action": "conv_face2girl", "error": str(ex)})
        time.sleep(5)
    # 一定時間待つ
    time.sleep(0.2)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        default="a young girl with detailed reflecting eyes by professional digital painting in granblue fantasy style, beautiful pretty cute face, full body shot of loli anime girl, a small smile, short blonde hair, big ribbon on the head, wearing fantasy clothes, front lighting, 8k resolution, featured on pixiv",
    )
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help="cap width", type=int, default=960)
    parser.add_argument("--height", help="cap height", type=int, default=540)

    parser.add_argument("--model_selection", type=int, default=0)
    parser.add_argument(
        "--min_detection_confidence",
        help="min_detection_confidence",
        type=float,
        default=0.7,
    )

    parser.add_argument("--use_brect", action="store_true")

    args = parser.parse_args()

    return args


def main():
    # 画像フォルダの作成
    image_dir = Path(IMAGE_DIR)
    image_dir.mkdir(exist_ok=True)
    # 引数解析 ###############################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    prompt = args.prompt

    model_selection = args.model_selection
    min_detection_confidence = args.min_detection_confidence

    use_brect = args.use_brect

    # StableDiffusionのAPIのインスタンスを作成 ############################
    api = webuiapi.WebUIApi(host="localhost", port=7860)
    # カメラ準備　###############################################################
    cap = cv.VideoCapture(cap_device, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード　###############################################################
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=model_selection,
        min_detection_confidence=min_detection_confidence,
    )

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    thread = None
    mode = None
    posX, posY, posCX, posCY, sizeW, sizeH = 0, 0, 0, 0, 0, 0

    while True:
        # カメラキャプチャ　###############################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # ミラー表示
        overlay_image = copy.deepcopy(image)

        # 検出実施　###############################################################
        # image = cv.cvtColor(image, cv.COLOR_RGB)
        results = face_detection.process(image)

        # 顔位置＆場所検出 ###############################################################
        if results.detections is not None:
            for detection in results.detections:
                # 検出された顔の場所を取得
                image, posX, posY, posCX, posCY, sizeW, sizeH = (
                    culculate_face_pos_and_size(image, detection)
                )
                # 顔の切り抜き画像を取得
                faceimage = trim_face(posX, posY, sizeW, sizeH, image)
                # thread開始
                if (
                    thread is None or not thread.is_alive()
                ):  # ThreadがNoneもしくはThreadが動いてなかったら
                    faceimage = Image.open(FACETRIM_IMAGE_PATH)
                    print("thread start")
                    thread = threading.Thread(
                        target=conv_face2girl,
                        args=(api, prompt, faceimage),
                    )
                    thread.start()

        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        if key == ord("1"):  # 美少女モード
            prompt = "a young girl with detailed reflecting eyes by professional digital painting in granblue fantasy style, beautiful pretty cute face, full body shot of loli anime girl, a small smile, short blonde hair, big ribbon on the head, wearing fantasy clothes, front lighting, 8k resolution, featured on pixiv"
            mode = "All Human Girls Mode"
        elif key == ord("2"):  # 美少年モード
            prompt = "super fine illustration, best quality, anime screencap, cowboy shot, 1 girl, brown hair, basketball court, team uniform, realistic, beautiful, anime, anime faces"
            mode = "All Human Boys Mode"
        elif key == ord("3"):  # おばあちゃんモード
            prompt = "masterpiece,high quality,(elder woman),a photo of female"
            mode = "All Human Obaa-Chan Mode"
        elif key == ord("4"):  # おじいちゃんモード
            prompt = "masterpiece,high quality,(elder man),a photo of male"
            mode = "All Human Ojii-Chan Mode"
        elif key == ord("5"):  # サイバーパンクモード
            prompt = "masterpiece, best quality, high resolution, cyberpunk anime style, beautiful VTuber, upper body, highly detailed face, glowing red cybernetic eyes, short silver bob cut, futuristic bodysuit with neon lines, cyber neon background, soft lighting, smooth shading"
            mode = "Cyberpunk Mode"
        # StableDiffusion返還後画像を重ねる
        cv.putText(
            image,
            mode,
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
            cv.LINE_AA,
        )
        overlay_image = overlay_illust(image, posCX, posCY, sizeH)
        # 画面反映 #############################################################
        cv.namedWindow("window", cv.WINDOW_NORMAL)
        cv.resizeWindow("window", int(960 * cap_width / cap_height), 960)
        cv.imshow("window", overlay_image)
    cap.release()
    cv.destroyAllWindows()


# 顔のx座標,y座標,x中心座標,y中心座標, 幅，高さを抽出　###############################################################
def culculate_face_pos_and_size(image, detection):
    image_width, image_height = image.shape[1], image.shape[0]
    bbox = detection.location_data.relative_bounding_box
    sizeW = int(bbox.width * image_width)  # 幅
    sizeH = int(bbox.height * image_height)  # 高さ
    posX = int(bbox.xmin * image_width)  # X座標
    posY = int(bbox.ymin * image_height)  # Y座標
    posCX = int(bbox.xmin * image_width + (sizeW / 2))  # X中心座標
    posCY = int(bbox.ymin * image_height + (sizeH / 2))  # Y中心座標

    # cv.putText(image, "posX:" + str(posX) + " posY:" + str(posY) + " sizeW" + str(sizeW) + " sizeH" + str(sizeH),
    #           (10,30),cv.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0),2,cv.LINE_AA)

    return image, posX, posY, posCX, posCY, sizeW, sizeH


# 重ね合わせ画像をresizeして透明化して重ねる
def overlay_illust(bg, posX, posY, sizeH):
    global g_olimage, g_is_image_updated
    try:
        if g_is_image_updated:
            g_olimage = cv.imread(CONVERTED_IMAGE_PATH, cv.IMREAD_UNCHANGED)
            with g_lock:
                g_is_image_updated = False
        resize_ol_image = cv.resize(
            g_olimage,
            dsize=None,
            fx=sizeH * 0.0035,
            fy=sizeH * 0.0035,
        )
        resize_ol_image_height = resize_ol_image.shape[0]
        resize_ol_image_width = resize_ol_image.shape[1]

        posY = posY - 50  # 高さ方向のオフセット

        # カメラ映像に重ね合わせ画像が入りきる場合は重ね合わせ
        if (
            (posY - (resize_ol_image_height / 2) > 0)
            & (posY + (resize_ol_image_height / 2) < bg.shape[0])
            & (posX - (resize_ol_image_width / 2) > 0)
            & (posX + (resize_ol_image_width / 2) < bg.shape[1])
        ):
            # bg[int(posY-(resize_ol_image_height/2)):int(posY+(resize_ol_image_height/2)),int(posX-(resize_ol_image_width/2)):int(posX+(resize_ol_image_width/2))] = (bg[int(posY-(resize_ol_image_height/2)):int(posY+(resize_ol_image_height/2)),int(posX-(resize_ol_image_width/2)):int(posX+(resize_ol_image_width/2))] * (1.0 - alpha)).astype('uint8') #透明度がMaxの箇所はBGR値を0に(黒に)
            # bg[int(posY-(resize_ol_image_height/2)):int(posY+(resize_ol_image_height/2)),int(posX-(resize_ol_image_width/2)):int(posX+(resize_ol_image_width/2))] = (bg[int(posY-(resize_ol_image_height/2)):int(posY+(resize_ol_image_height/2)),int(posX-(resize_ol_image_width/2)):int(posX+(resize_ol_image_width/2))] + (laugh_man_color * alpha)).astype('uint8') #合成
            bg[
                int(posY - (resize_ol_image_height / 2)) : int(
                    posY + (resize_ol_image_height / 2),
                ),
                int(posX - (resize_ol_image_width / 2)) : int(
                    posX + (resize_ol_image_width / 2),
                ),
            ] = resize_ol_image
        return bg
    except Exception as ex:
        print({"action": "overlay_illust", "error": str(ex)})
        return bg


# 顔の部分を切り抜き()
def trim_face(posX, posY, sizeW, sizeH, image):
    try:
        faceimage = image[posY - 100 : posY + sizeH, posX - 50 : posX + sizeW + 50]
        cv.imwrite(FACETRIM_IMAGE_PATH, faceimage)
        return faceimage
    except Exception:
        # print(ex)
        return image


if __name__ == "__main__":
    main()
