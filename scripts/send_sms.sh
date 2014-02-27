#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    echo "
    Send a fake SMS to TTS

    Usage:

        # sms-send.sh [-h HOST] [-n NUMBER] [-P PORT] [MESSAGE...]

    -h  host (default: $(hostname -i ))
    -n  number (default: +44700900000)
    -p  port (default: 8080)

    MESSAGE
        SMS content. If not given, a short message is selected at
        random.
"
    exit 1
}

messages=(
    'I have been to the dark side of the moon'
    'Tomorrow I am going to the super market'
    'Why not put your finger in the socket'
    'Do is matter that I have lost my SIM card'
    'Take this to the cleaners I spilt concrete on it'
    'This is the last time I tell you do not fall over'
)


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
    message=$(
        for m in "${messages[@]}"; do
            echo $m
        done | shuf -n 1
    )
else
    message="${*}"
fi

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

curl --verbose \
     -d "number=${number}" \
     -d "message=${message}" \
     "http://${host}:${port}/"

echo


