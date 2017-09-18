#!/bin/bash

function __test_clone () {
    bash run.sh --clone __test__ -p
}
function __test_build () {
    bash run.sh --build __test__ -p
}

function __assert_tests () {
    __test_clone
    dir="$HOME/__test__"
    if [ -d "$dir" ]; then
        echo "[ OK ] ... test_clone successfull"
    else
        echo "[WARN] ... test_clone failed"
        echo "Exiting tests ..."
        return 1
    fi
    __test_build
    file="$dir/output"
    if [ -f "$file" ]; then
        echo "[ OK ] ... test_build successfull"
        return 0
    else
        echo "[WARN] ... test_build failed"
        return 1
    fi
    echo "end tests"
}

function __clear_tests () {
    dir="$HOME/__test__"
    rm -rf $dir
}

__assert_tests
__clear_tests
