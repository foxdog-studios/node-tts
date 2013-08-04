#!/bin/bash

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/../..")

SETUP="${REPO}/scripts/setup"

VE2="${REPO}/env2"
VE3="${REPO}/env3"

AUR_PACKAGES=(
    fluidr3
)

SYSTEM_PACKAGES=(
    alsa-oss
    fluidsynth
    python-virtualenv
    python2-virtualenv
    sox
)

_install_python_packages()
{
    pip install --requirement "${1}"
}

_ve_on()
{
    local before=$(set +o | grep nounset)
    set +o nounset
    source "${1}/bin/activate"
    ${before}
}

build_phonemes()
{
    ve2_on
    python "${REPO}/scripts/build_phonemes.py"
    ve_off
}

create_ves()
{
    virtualenv-2.7 "${VE2}"
    virtualenv-3.3 "${VE3}"
}

install_aur_packages()
{
    yaourt --noconfirm --needed --sync --refresh "${AUR_PACKAGES[@]}"
}

install_python2_packages()
{
    ve2_on
    _install_python_packages "${SETUP}/requirement-python2.txt"
    ve_off
}

install_python3_packages()
{
    ve3_on
    _install_python_packages "${SETUP}/requirement.txt"
    ve_off
}

install_python3_packages_devel()
{
    ve3_on
    _install_python_packages "${SETUP}/requirement-devel.txt"
    ve_off

    (
        cd -- "${VE3}/bin"
        ln -fs ipython3 ipython
    )
}

install_system_packages()
{
    sudo pacman --noconfirm --needed --sync --refresh "${SYSTEM_PACKAGES[@]}"
}

render_midi_files()
{
    local midi wav
    pushd .
    cd -- "${REPO}/backing_tracks"

    for midi in *.mid; do
        wav="${midi%.mid}"
        "${REPO}/scripts/midi-render.sh" "${midi}" "${wav}.wav"
    done

    ln -fs popcorn.wav default.wav

    popd
}

ve_off()
{
    local before=$(set +o | grep nounset)
    set +o nounset
    deactivate
    ${before}
}

ve3_on()
{
    _ve_on "${VE3}"
}

ve2_on()
{
    _ve_on "${VE2}"
}

