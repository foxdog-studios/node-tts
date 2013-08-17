#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    echo "
    Install dependencies and setup environment

    Usage:

        # $(basename "${0}") [-a]

    -a  install AUR packages
"
    exit 1
}

call_install_aur_packages=false

while getopts :a opt; do
    case "${opt}" in
        a) call_install_aur_packages=true ;;
        \?|*) usage ;;
    esac
done
unset opt

shift $(( $OPTIND - 1 ))

if [[ "${#}" != 0 ]]; then
    usage
fi
unset usage

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")
cd -- "${REPO}"

source scripts/setup/_arch.sh

install_system_packages
if $call_install_aur_packages; then
    install_aur_packages
fi
unset call_install_aur_packages
install_node_modules
install_bower_components
create_ves
install_python2_packages
install_python3_packages
install_python3_packages_devel
render_midi_files
build_phonemes

