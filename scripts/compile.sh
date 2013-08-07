#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
"${REPO}/scripts/sms-send.sh" -h 192.168.1.65 -n admin compile

