# Commandline arguments for webui.py, for example: export COMMANDLINE_ARGS="--medvram --opt-split-attention"
export COMMANDLINE_ARGS="--api --listen"

cd "$(dirname "$0")/../submodules/stable-diffusion-webui" && bash webui.sh
