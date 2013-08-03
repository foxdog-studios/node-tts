#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")

VE="${REPO}/env"

SYSTEM_PACKAGES=(
    python-virtualenv
)

create_ve()
{
    virtualenv-3.3 "${VE}"
}

install_system_packages()
{
    sudo pacman --noconfirm --needed --sync --refresh "${SYSTEM_PACKAGES[@]}"
}

install_python_packages()
{
    ve_on
    pip install -r "${REPO}/requirement.txt"
    ve_off
}

ve_off()
{
    set +o nounset
    deactivate
    set -o nounset
}

ve_on()
{
    set +o nounset
    source "${VE}/bin/activate"
    set -o nounset
}

