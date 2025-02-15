import webuiapi
from PIL import Image

# APIのインスタンスを作成 ############################
api = webuiapi.WebUIApi()
# プロンプトを宣言 ##################################
PROMPT= "masterpiece, best quality, shinkai makoto, boy"
faceimage = Image.open("tests/stable_diffusion_tests/images/facetrim.png")   

girlimage = api.img2img(images = [faceimage], prompt=PROMPT, seed=5555, cfg_scale=6.5, denoising_strength=0.5)
# 画像を保存する
girlimage.image.save("tests/stable_diffusion_tests/images/girlimage.png")
