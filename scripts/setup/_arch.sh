#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")

VE="${REPO}/env"

SYSTEM_PACKAGES=(
    alsa-oss
    fluidr3
    fluidsynth
    python-virtualenv
    sox
)

_install_python_packages()
{
    ve_on
    pip install --requirement "${1}"
    ve_off
}

create_ve()
{
    virtualenv-3.3 "${VE}"
}

install_system_packages()
{
    yaourt --noconfirm --needed --sync --refresh "${SYSTEM_PACKAGES[@]}"
}

install_python_packages()
{
    _install_python_packages "${REPO}/requirement.txt"
}

install_python_packages_devel()
{
    pushd .
    cd -- "${VE}/bin"

    _install_python_packages "${REPO}/requirement-devel.txt"
    ln -fs ipython3 ipython

    popd
}

render_midi_files()
{
    local midi wav
    pushd .
    cd -- "${REPO}/backing_tracks"

    for midi in *.mid; do
        wav="${midi%.mid}"
        "${REPO}/scripts/backing-track-render.sh" "${midi}" "${wav}.wav"
    done

    ln -fs popcorn.wav default.wav

    popd
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

