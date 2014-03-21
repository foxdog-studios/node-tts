#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET


# ==============================================================================
# = Configuration                                                              =
# ==============================================================================

repo=$(realpath -- ${0:h}/..)

venv=$repo/local/venv

pacman_packages=(
    git
    python2-virtualenv
    zsh
)


# ==============================================================================
# = Tasks                                                                      =
# ==============================================================================

function install_pacman_packages()
{
    sudo pacman --noconfirm --sync --needed --refresh $pacman_packages
}

function create_virtualenv()
{
    mkdir --parents $venv:h
    virtualenv --python=python2.7 $venv
}

function install_python_packages()
{
    unsetopt NO_UNSET
    source $venv/bin/activate
    setopt NO_UNSET

    pip install --requirement $repo/requirements.txt
}

function init_local()
{
    local config_dir=$repo/local/config
    local dev_dir=$config_dir/development

    mkdir --parents $dev_dir

    local config_name=tts.yaml
    if [[ ! -e $dev_dir/$config_name ]]; then
        cp $repo/templates/$config_name $dev_dir
    fi

    local target=$config_dir/default
    if [[ ! -e $target ]]; then
        ln --force --symbolic $dev_dir:t $target
    fi
}


# ==============================================================================
# = Command line interface                                                     =
# ==============================================================================

tasks=(
    install_pacman_packages
    create_virtualenv
    install_python_packages
    init_local
)

function usage()
{
    cat <<-'EOF'
		Set up a development environment

		Usage:

		    setup.zsh [TASK...]

		Tasks:

		    install_pacman_packages
		    create_virtualenv
		    install_python_packages
		    init_local
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

