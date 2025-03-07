<!-- omit in toc -->
# human-galgee-system-ailab

人類ギャルゲー化システムのリポジトリです。\
このリポジトリは、<https://github.com/gakutosasabe/HearExpansion>をベースに作成しています。

<!-- omit in toc -->
## 目次

- [1. インストール（for Ubuntu）](#1-インストールfor-ubuntu)
  - [1.1. Pythonのインストール](#11-pythonのインストール)
  - [1.2. Poetryのインストール](#12-poetryのインストール)
  - [1.3. 依存パッケージのインストール](#13-依存パッケージのインストール)
  - [1.4. サブモジュールのクローン](#14-サブモジュールのクローン)
  - [1.5. Stable Diffusionのセットアップ](#15-stable-diffusionのセットアップ)
    - [1.5.1. CUDAのインストール](#151-cudaのインストール)
    - [1.5.2. Stable Diffusion WebUIのインストール](#152-stable-diffusion-webuiのインストール)
    - [1.5.3. Stable Diffusion WebUIの動作確認](#153-stable-diffusion-webuiの動作確認)
- [2. 起動](#2-起動)

## 1. インストール（for Ubuntu）

**Ubuntu24.04用のインストール手順です。**\
※Windows用のインストール手順は[こちら](README.md)を参照してください。

### 1.1. Pythonのインストール

pyenvを使用してPythonをインストールします。

```bash
sudo apt update
sudo apt install build-essential libffi-dev libssl-dev zlib1g-dev liblzma-dev libbz2-dev libreadline-dev libsqlite3-dev libopencv-dev tk-dev git
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo '' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
source ~/.bashrc
pyenv -v
```

Python3.11.4をインストールする例

```bash
pyenv install --list
pyenv install 3.11.4
pyenv versions
pyenv global 3.11.4
python --version
pip --version
```

参考URL：<https://microai.jp/blog/9b3280f8-4a92-41e5-a54e-08d518441235>

### 1.2. Poetryのインストール

PoetryとはPythonの依存関係の管理とパッケージ化のためのツールで、npmのPythonバージョンのようなものです。

```bash
pip install pipx
pipx install poetry
pipx ensurepath
source ~/.bashrc
poetry --version
poetry self update
poetry config virtualenvs.in-project true
```

### 1.3. 依存パッケージのインストール

リポジトリのルートディレクトリで以下のコマンドを実行します。

```bash
poetry install
```

### 1.4. サブモジュールのクローン

ターミナルを開いて以下を実行する。

```bash
git submodule update --init
```

### 1.5. Stable Diffusionのセットアップ

Stable Diffusionが動作するようにセットアップします。

#### 1.5.1. CUDAのインストール

CUDAがインストールされていない場合は、インストールします。\
[こちら](https://www.notion.so/Ubuntu24-04-CUDA-19bcdce3b6f8809ea455cd1bef37917c?pvs=4)の手順を参照してください。

ターミナルで`nvidia-smi`コマンドを実行してインストールされているか確認できます。

```bash
$ nvidia-smi
Sat Feb 15 18:33:40 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.86.15              Driver Version: 570.86.15      CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2060        Off |   00000000:01:00.0 Off |                  N/A |
| N/A   50C    P0             21W /   90W |    2922MiB /   6144MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
...
```

#### 1.5.2. Stable Diffusion WebUIのインストール

Stable Diffusion WebUIをインストールします。

ターミナルで以下のスクリプトを実行します。

```bash
./bin/run-stable-diffusion-webui.sh
```

#### 1.5.3. Stable Diffusion WebUIの動作確認

以下のコマンドでStable Diffusion WebUIの動作確認を行います。

```bash
poetry run python tests/stable_diffusion_tests/python_sd_test.py
```

`tests/stable_diffusion_tests/images/testsd3.png`が生成されていればOKです。

## 2. 起動

以下の手順で起動します。

1. Stable Diffusion WebUIが起動していなければ、起動します。

    ```bash
    ./bin/run-stable-diffusion-webui.sh
    ```

1. 人類ギャルゲー化システムを起動します。

    ```bash
    poetry run python -m human_galgee_system
    ```

    ※VSCodeで`human-galgee-system-ailab.code-workspace`を開いている場合は、上記コマンドに変わって「F5」キーでデバッグ実行が可能です。
