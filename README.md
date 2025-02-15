<!-- omit in toc -->
# human-galgee-system-ailab

人類ギャルゲー化システムのリポジトリです。\
このリポジトリは、<https://github.com/gakutosasabe/HearExpansion>をベースに作成しています。

<!-- omit in toc -->
## 目次

- [1. インストール](#1-インストール)
  - [1.1. Pythonのインストール](#11-pythonのインストール)
    - [1.1.1. Windowsの場合](#111-windowsの場合)
    - [1.1.2. Ubuntuの場合](#112-ubuntuの場合)
  - [1.2. Poetryのインストール](#12-poetryのインストール)
    - [1.2.1. Windowsの場合](#121-windowsの場合)
    - [1.2.2. Ubuntuの場合](#122-ubuntuの場合)
  - [依存パッケージのインストール](#依存パッケージのインストール)
  - [1.3. サブモジュールのクローン](#13-サブモジュールのクローン)
  - [1.4. Stable Diffusionのセットアップ](#14-stable-diffusionのセットアップ)
    - [1.4.1. Stable Diffusion WebUIのインストール](#141-stable-diffusion-webuiのインストール)
      - [1.4.1.1. Windowsの場合](#1411-windowsの場合)
      - [1.4.1.2. Ubuntuの場合](#1412-ubuntuの場合)
    - [1.4.2. Stable Diffusion WebUIの動作確認](#142-stable-diffusion-webuiの動作確認)
- [起動](#起動)

## 1. インストール

以下の手順でインストールします。

### 1.1. Pythonのインストール

#### 1.1.1. Windowsの場合

Python3.10以上がインストールされていない場合は、以下を参考にダウンロード・インストールします。\
<https://www.javadrive.jp/python/install/index1.html>

#### 1.1.2. Ubuntuの場合

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

#### 1.2.1. Windowsの場合

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

#### 1.2.2. Ubuntuの場合

```bash
pip install pipx
pipx install poetry
pipx ensurepath
source ~/.bashrc
poetry --version
poetry self update
poetry config virtualenvs.in-project true
```

### 依存パッケージのインストール

リポジトリのルートディレクトリで以下のコマンドを実行します。

```bash
poetry install
```

### 1.3. サブモジュールのクローン

ターミナルを開いて以下を実行する。

```bash
git submodule update --init
```

### 1.4. Stable Diffusionのセットアップ

Stable Diffusionが動作するようにセットアップします。

#### 1.4.1. Stable Diffusion WebUIのインストール

Stable Diffusion WebUIをインストールします。

##### 1.4.1.1. Windowsの場合

ターミナルで以下のスクリプトを実行します。

```powershell
.\bin\run-stable-diffusion-webui.bat
```

##### 1.4.1.2. Ubuntuの場合

`submodules/stable-diffusion-webui/webui-user.sh`を編集します。

```bash
cd submodules/stable-diffusion-webui/
vim webui-user.sh
```

13行目に`--api`と`--list`オプションを追記します。

```bash
# Commandline arguments for webui.py, for example: export COMMANDLINE_ARGS="--medvram --opt-split-attention"
export COMMANDLINE_ARGS="--api --listen"
```

ターミナルで実行します。

```powershell
cd submodules/stable-diffusion-webui/
./webui.sh
```

#### 1.4.2. Stable Diffusion WebUIの動作確認

以下のコマンドでStable Diffusion WebUIの動作確認を行います。

```bash
poetry run python tests/stable_diffusion_tests/python_sd_test.py
```

ルートディレクトリに`testsd3.png`が生成されていればOKです。

## 起動

以下の手順で起動します。

1. Stable Diffusion WebUIが起動していなければ、起動します。

    ```bash
    .\bin\run-stable-diffusion-webui.bat
    ```

1. 人類ギャルゲー化システムを起動します。

    ```bash
    poetry run python .\human_galgee_system\main.py
    ```
