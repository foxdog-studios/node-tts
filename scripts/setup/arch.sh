#!/bin/bash

set -o errexit
set -o nounset

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")

source scripts/setup/_arch.sh

install_system_packages
create_ve
install_python_packages
install_python_packages_devel
render_midi_files

