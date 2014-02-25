#!/usr/bin/env zsh

setopt err_exit
setopt no_unset


# =============================================================================
# = Command line interface                                                    =
# =============================================================================

function usage()
{
    cat <<-'EOF'
		Build dino

		Usage:

			$ dino-build.zsh
	EOF
    exit 1
}

if [[ $# -ne 0 ]]; then
    usage
fi


# =============================================================================
# = Configuration                                                             =
# =============================================================================

repo=$(realpath -- ${0:h}/..)
bundle_name=bundle
build_dir=$repo/local/build
bundle_archive=$build_dir/$bundle_name.tar.gz
bundle_dir=$build_dir/$bundle_name


# =============================================================================
# = Build                                                                     =
# =============================================================================

# Remove old build
rm --force --recursive $build_dir
mkdir --parents $build_dir

cd $build_dir

# Create bundle
$repo/scripts/dino.zsh bundle $bundle_archive

# Unbundle
tar --extract --file $bundle_archive

# Reinstall fibers
(
    cd $bundle_dir/programs/server/node_modules
    rm --force --recursive fibers
    npm install fibers
)

