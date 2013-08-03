#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")

compile()
{
    "${REPO}/scripts/sms-send.sh" -n admin compile
}

