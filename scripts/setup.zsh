#!/usr/bin/env zsh

setopt err_exit
setopt no_unset


# ==============================================================================
# = Configuration                                                              =
# ==============================================================================

repo=$(realpath -- ${0:h}/..)

env=$repo/env

global_node_packages=(
    meteorite
)

pacman_packages=(
    git
    nodejs
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

function install_meteor()
{
   curl https://install.meteor.com/ | sh
}

function install_global_node_packages()
{
    sudo --set-home npm install --global $global_node_packages
}

function install_meteorite_packages()
{(
    cd $repo/meteor
    mrt install
)}

function create_ve()
{
    virtualenv-2.7 $env
}

function install_python_packages()
{(
    unsetopt no_unset
    source $env/bin/activate
    set no_unset

    pip install git+https://github.com/foxdog-studios/pyddp.git
    pip install --requirement $repo/requirement.txt
)}

function init_local()
{
    local config_dir=$repo/local/config
    local dev_dir=$config_dir/development
    local template_dir=$repo/templates

    mkdir --parents $dev_dir

    local tts_name=tts.yaml
    if [[ ! -e $dev_dir/$tts_name ]]; then
        cp $template_dir/$tts_name $dev_dir
    fi

    local dino_name=dino.json
    if [[ ! -e $dev_dir/$dino_name ]]; then
        cp $template_dir/$dino_name $dev_dir
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
    create_ve
    install_python_packages
    install_meteor
    install_global_node_packages
    install_meteorite_packages
    init_local
)

function usage()
{
    cat <<-'EOF'
		Set up a development environment

		Usage:

		    setup.sh [TASK...]

		Tasks:

		    install_pacman_packages
		    create_ve
		    install_python_packages
		    install_meteor
		    install_global_node_packages
		    install_meteorite_packages
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
    echo -e "\e[5;32mTask: $task\e[0m\n"
    $task
done

