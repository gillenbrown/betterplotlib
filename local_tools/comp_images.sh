#!/bin/bash
# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEST_DIR="$( dirname $SCRIPT_DIR)/testing"
open $TEST_DIR/baseline_images/$1.png $TEST_DIR/temporary_images/$1.png