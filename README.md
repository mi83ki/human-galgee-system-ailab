<!-- omit in toc -->
# human-galgee-system-ailab

人類ギャルゲー化システムのリポジトリです。\
このリポジトリは、<https://github.com/gakutosasabe/HearExpansion>をベースに作成しています。

<!-- omit in toc -->
## 目次

- [1. インストール（for Windows）](#1-インストールfor-windows)
  - [1.1. Pythonのインストール](#11-pythonのインストール)
  - [1.2. Poetryのインストール](#12-poetryのインストール)
  - [1.3. 依存パッケージのインストール](#13-依存パッケージのインストール)
  - [1.4. サブモジュールのクローン](#14-サブモジュールのクローン)
  - [1.5. Stable Diffusionのセットアップ](#15-stable-diffusionのセットアップ)
    - [1.5.1. CUDAのインストール](#151-cudaのインストール)
    - [1.5.2. Stable Diffusion WebUIのインストール](#152-stable-diffusion-webuiのインストール)
    - [1.5.3. Stable Diffusion WebUIの動作確認](#153-stable-diffusion-webuiの動作確認)
- [2. 起動](#2-起動)

## 1. インストール（for Windows）

**Windows用のインストール手順です。**\
※Ubuntu用のインストール手順は[こちら](README_UBUNTU.md)を参照してください。

### 1.1. Pythonのインストール

Python3.10以上がインストールされていない場合は、以下を参考にダウンロード・インストールします。\
<https://www.javadrive.jp/python/install/index1.html>

### 1.2. Poetryのインストール

PoetryとはPythonの依存関係の管理とパッケージ化のためのツールで、npmのPythonバージョンのようなものです。

PowerShellを開いて以下を実行します。

```PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

環境変数を追加します。

```PowerShell
[System.Environment]::SetEnvironmentVariable('path', $env:APPDATA + "\pypoetry\venv\Scripts;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```

再度PowerShellを開き直して、以下を実行します。

```PowerShell
poetry --version
poetry self update
poetry config virtualenvs.in-project true
```

※もしpoetryが登録されていない場合は、環境変数の`Path`に以下を追加してみてください。\
参考URL：<https://zenn.dev/kkj/articles/d14470babe1930>

```text
%APPDATA%\Python\Scripts
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
[こちら](https://www.notion.so/Windows-AI-955a13b7877c4346a81531c7820d7c7b?pvs=4)の手順を参照してください。

ターミナルで`nvidia-smi`コマンドを実行してインストールされているか確認できます。

```bash
> nvidia-smi
Sat Feb 15 18:31:37 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.94                 Driver Version: 560.94         CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2060 ...  WDDM  |   00000000:2B:00.0  On |                  N/A |
| 29%   37C    P8             22W /  175W |    4573MiB /   8192MiB |     16%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
...
```

#### 1.5.2. Stable Diffusion WebUIのインストール

Stable Diffusion WebUIをインストールします。

ターミナルで以下のスクリプトを実行します。

```powershell
.\bin\run-stable-diffusion-webui.bat
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
    .\bin\run-stable-diffusion-webui.bat
    ```

1. 人類ギャルゲー化システムを起動します。

    ```bash
    poetry run python -m human_galgee_system
    ```

    ※VSCodeで`human-galgee-system-ailab.code-workspace`を開いている場合は、上記コマンドに変わって「F5」キーでデバッグ実行が可能です。
