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
    killall -9 chromium node python || true
}

trap clean_up SIGINT SIGTERM EXIT


# =============================================================================
# = Helpers                                                                   =
# =============================================================================

term() {
    xterm -e "${@}" & disown
}

term_hold() {
    xterm -hold & disown
}

term ./scripts/run.sh

term grunt

term_hold

chromium --incognito http://localhost:8000

