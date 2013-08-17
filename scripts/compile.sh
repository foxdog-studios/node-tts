#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
"${REPO}/scripts/sms-send.sh" -h "$(hostname -i)" -n admin compile

