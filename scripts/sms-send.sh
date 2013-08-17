#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    host=$(hostname -i)
    echo "
    Send a fake SMS to TTS

    Usage:

        # sms-send.sh [-h HOST] [-n NUMBER] [-P PORT] MESSAGE...

    -h  host (default: ${host})
    -n  number (default: +44700900000)
    -p  port (default: 8080)

    MESSAGE
        SMS content
"
    exit 1
}

host=$(hostname -i)
number=+44700900000
port=8080

while getopts :h:n:p: opt; do
    case "${opt}" in
        h) host="${OPTARG}" ;;
        n) number="${OPTARG}" ;;
        p) port="${OPTARG}" ;;
        \?|*) usage ;;
    esac
done

shift $(( $OPTIND - 1 ))

if [[ $# == 0 ]]; then
    usage
fi

message="${*}"

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

curl --verbose \
     -d "number=${number}" \
     -d "message=${message}" \
     "http://${host}:${port}/"

echo

