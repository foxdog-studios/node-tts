#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    echo "


    Usage:

        # $(basename "${0}") [-]
"
    exit 1
}

while getopts : opt; do
    case "${opt}" in
        \?|*) usage ;;
    esac
done
unset opt

shift $(( OPTIND - 1 ))

if [[ "${#}" != 0 ]]; then
    usage
fi
unset usage

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

# =============================================================================
# = Clean-up                                                                  =
# =============================================================================

clean_up() {
    killall -9 node python || true
}

trap clean_up EXIT


# =============================================================================
# = Helpers                                                                   =
# =============================================================================

term() {
    xterm -hold -e "${@}" &
}

term ./scripts/run.sh

term grunt

konsole &

sleep 2
chromium --incognito --user-data-dir=/tmp http://localhost:8000

