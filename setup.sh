#!/bin/bash

root_dir="$(dirname "${BASH_SOURCE[0]}")"
cd "$root_dir"

(
set -e
if [[ ! -d "$root_dir"/conda ]]; then
    case "$(uname -s)" in
        Linux)
            os=Linux-$(uname -p)
            ;;
        Darwin)
            os=MacOSX-x86_64 # uname -p on macOS returns i386 even though it's a 64-bit processor
            ;;
        *)
            echo "Unable to detect OS ($(uname -s)), aborting."
            exit 1
            ;;
    esac
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-$os.sh -O conda-installer.sh
    bash ./conda-installer.sh -b -p "$root_dir"/conda
    rm conda-installer.sh
    source "$root_dir"/conda/etc/profile.d/conda.sh
    conda create -y -p "$root_dir"/conda/envs/myenv python=3.7

    cat > "$root_dir"/env.sh <<EOF
source "$root_dir"/conda/etc/profile.d/conda.sh
conda activate "$root_dir"/conda/envs/myenv
EOF
fi
)

if [[ -f "$root_dir"/env.sh ]]; then
    source "$root_dir"/env.sh
fi

# pip install -e .
# pip install -r requirements-dev.txt
# ./run_tests
