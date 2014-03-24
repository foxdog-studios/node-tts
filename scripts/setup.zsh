#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET


# ==============================================================================
# = Configuration                                                              =
# ==============================================================================

# Paths

repo=$(realpath -- ${0:h}/..)


# Packages

global_node_packages=(
    node-gyp
)

pacman_packages=(
    git
    python2
    yaourt
    zsh
)


# ==============================================================================
# = Tasks                                                                      =
# ==============================================================================

function install_pacman_packages()
{
    sudo pacman --noconfirm --sync --needed --refresh $pacman_packages
}

function install_swift()
{
    if pacman -Q swift &> /dev/null; then
        return
    fi

    if [[ ! -d /tmp/swift ]]; then
        git clone gitolite@foxdogstudios.com:swift /tmp/swift
    fi

    cd /tmp/swift
    make rebuild
    sudo pacman --noconfirm --upgrade *pkg.tar.xz
}

function install_global_node_packages()
{
    sudo --set-home npm install --global $global_node_packages
}


# ==============================================================================
# = Command line interface                                                     =
# ==============================================================================

tasks=(
    install_pacman_packages
    install_swift
    install_global_node_packages
)

function usage()
{
    cat <<-'EOF'
		Set up a development environment

		Usage:

		    setup.zsh [TASK...]

		Tasks:

		    install_pacman_packages
		    install_swift
		    install_global_node_packages
	EOF
    exit 1
}

for task in $@; do
    if [[ ${tasks[(i)$task]} -gt ${#tasks} ]]; then
        usage
    fi
done

for task in ${@:-$tasks}; do
    print -P -- "%F{green}Task: $task%f"
    $task
done

