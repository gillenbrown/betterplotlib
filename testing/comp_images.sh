#!/bin/bash
# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
open $SCRIPT_DIR/baseline_images/$1.png $SCRIPT_DIR/temporary_images/$1.png