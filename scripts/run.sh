#!/bin/bash

set -o errexit
set -o nounset

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

set +o nounset
source env/bin/activate
set -o nounset

python src/tts.py "${@}"

