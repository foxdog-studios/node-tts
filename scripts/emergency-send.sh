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

./scripts/sms-send.sh "if only we could fly limp bizkit style take them to the
matthews bridge john otto do you know where you are welcome to the jungle punk
take a look around because limp bizkit is fucking up your town we download on
the shockwaves for the ladies in the caves to get their groove on maybee im not
a wonderffuuuul lover but guess who next the cuckkoos nest talkin about my
generation generation x generation straange the sun dont even shie throught our
window pane"
./scripts/compile.sh

