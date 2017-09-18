#!/bin/bash

function __test_clone () {
    bash run.sh --clone __test__ -p
}
function __test_build () {
    bash run.sh --build __test__ -p
}

function __test_make () {
    bash run.sh --make $PWD
}

function __clear_tests () {
    dir="$HOME/__test__"
    rm -rf $dir
}

function __assert_tests_1 () {
    dir="$HOME/__test__"
    if [ -d "$dir" ]; then
        echo "[ OK ] ... test_clone successfull"
    else
        echo "[WARN] ... test_clone failed"
        echo "Exiting tests ..."
        exit 1
    fi
    file="$dir/output"
    if [ -f "$file" ]; then
        echo "[ OK ] ... test_build successfull"
    else
        echo "[WARN] ... test_build failed"
        exit 1
    fi
    echo "end tests"
}

function __assert_tests_2 () {
  dir="$HOME/__test__"
  if [ -d "$dir" ]; then
      echo "[ OK ] ... test_make part clone successfull"
  else
      echo "[WARN] ... test_make part clone failed"
      echo "Exiting tests ..."
      exit 1
  fi
  file="$dir/output"
  if [ -f "$file" ]; then
      echo "[ OK ] ... test_make part build  successfull"
  else
      echo "[WARN] ... test_make part build failed"
      exit 1
  fi
  echo "end tests"
}

function run_tests () {
    echo 'Runing normal tests'
    __test_clone
    __test_build
    __assert_tests_1
    __clear_tests
    echo 'Runing make tests'
    __test_make
    __assert_tests_2
    __clear_tests
}

run_tests
