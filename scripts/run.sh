# Python
export PYTHONPATH="$(pwd):$PYTHONPATH"

source scripts/env.sh

python3.12 exchange/cli.py
