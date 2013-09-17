#!/bin/bash

set -o errexit
set -o nounset


# =============================================================================
# = Command line interface                                                    =
# =============================================================================

check_network_connection=true
configure_audio=true
configure_displays=true
launch_grunt=true
launch_server=true
launch_viewer=true
layout_windows=true
perform_clean_up=true
perform_sanity_checks=true

usage() {
    echo "
    Run tts in a gig context


    Usage:

        # gig.sh [-ACDGNPSVW]

    -A  do not configure audio
    -C  do not perform pre or post clean up
    -D  do not configure displays
    -G  do not launch grunt
    -N  do not check network connection
    -P  do not perform sanity checks
    -S  do not launch server
    -V  do not launch viewer
    -W  do not layout windows
"
    exit 1
}

while getopts :ACDGNPSVW opt; do
    case "${opt}" in
        A) configure_audio=false ;;
        C) perform_clean_up=false ;;
        D) configure_displays=false ;;
        G) launch_grunt=false ;;
        N) check_network_connection=false ;;
        P) perform_sanity_checks=false ;;
        S) launch_server=false ;;
        V) launch_viewer=false ;;
        W) layout_windows=false ;;
        \?|*) usage ;;
    esac
done

shift $(( OPTIND - 1 ))

if [[ "${#}" != 0 ]]; then
    usage
fi


# =============================================================================
# = Helpers                                                                   =
# =============================================================================

num_logs=0

start() {
    num_logs=$[ num_logs + 1 ]
    echo -n "${num_logs}) ${*} ..."
}

complete() {
    echo -en "\r\e[K\e[1;32m"
    echo -n "${num_logs}) ${1}"
    echo -e "\e[0m"
}

wait_port() {
    until netstat -tln | tr -s ' ' | cut -d ' ' -f 4 | grep -q ":${1}$"; do
        sleep 0.1
    done
}


# =============================================================================
# = Clean up                                                                  =
# =============================================================================

if $perform_clean_up; then
    clean_up() {
        start 'Performing clean up'
        killall -9 -q chrome node python || true
        xdotool key alt+shift+space
        complete 'Clean up performed'
    }
    trap clean_up EXIT
    clean_up
fi


# =============================================================================
# = Working directory                                                         =
# =============================================================================

start 'Setting working diirectory'
repo=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${repo}"
complete 'Working directory set'


# =============================================================================
# = Checking network connection                                               =
# =============================================================================

if $check_network_connection; then
    start 'Checking network connection'; echo
    # Ping eldog's Android device
    ping -q -c 1 192.168.1.148
    complete 'Connected to network'
fi


# =============================================================================
# = Sanity checks                                                             =
# =============================================================================

if $perform_sanity_checks; then
    start 'Performing sanity checks'; echo
    ask() {
        prompt=$(echo -en "\e[5;91m"; echo -n "${*} "; echo -e "\e[0m")
        read -p "${prompt}"
    }
    ask 'Start SMS Proxy'
    ask 'Check AB box is normally on'
    complete 'Performing sanity checks'
fi


# =============================================================================
# = Audio                                                                     =
# =============================================================================

if $configure_audio; then
    start 'Configuring audio'
    amixer -q set Master 100%
    amixer -q set Master unmute
    complete 'Audio configured'
fi


# =============================================================================
# = Displays                                                                  =
# =============================================================================

if $configure_displays; then
    start 'Configuring displays'
    mode=1024x768
    xrandr --output LVDS1 --mode "${mode}"                                    \
           --output VGA1  --mode "${mode}" --same-as LVDS1
    complete 'Displays configured'
fi


# =============================================================================
# = Grunt                                                                     =
# =============================================================================

if $launch_grunt; then
    start 'Starting grunt'
    konsole --workdir "${repo}" -e grunt
    wait_port 8000
    complete 'Grunt started'
fi


# =============================================================================
# = Server                                                                    =
# =============================================================================

if $launch_server; then
    start 'Launching server'; echo
    konsole -e "${repo}/scripts/run.sh"
    wait_port 8080
    complete 'Server launched'
fi


# =============================================================================
# = Viewer                                                                    =
# =============================================================================

if $launch_viewer; then
    start 'Launching viewer'; echo
    google-chrome --incognito                                                 \
                  --kiosk                                                     \
                  http://localhost:8000/ &
    until wmctrl -a 'Google Chrome'; do
        sleep 0.1
    done
    complete 'Viewer launched'
fi


# =============================================================================
# = Layout windows                                                            =
# =============================================================================

if $layout_windows; then
    start 'Laying out windows'
    xdotool key alt+shift+space                                               \
            key alt+space                                                     \
            key alt+space                                                     \
            key alt+ctrl+x
    complete 'Windows layed out'
fi


# =============================================================================
# = Wait                                                                      =
# =============================================================================

read -p "$(echo -e '\e[34mPress RETURN to exit\e[0m ')"

