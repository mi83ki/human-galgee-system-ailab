@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--api --listen

cd /d "%~dp0..\submodules\stable-diffusion-webui"
call webui.bat
