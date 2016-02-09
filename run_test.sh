#!/bin/bash


function go_to_dirname
{
    echo "Go to working directory..."
    cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    if [ $? -ne 0 ]
    then
        echo "go_to_dirname failed";
        exit 1
    fi
    echo "-> Current directory is" $(pwd)
}

function run_tests
{
    export LC_ALL=C
    set -x
    python -m unittest discover $(pwd)/scripts/haproxy
    if [ $? -ne 0 ]
    then
        exit 2
    fi
    python -m unittest discover $(pwd)/scripts/heat_tools
    if [ $? -ne 0 ]
    then
        exit 3
    fi
    cd $(pwd)/scripts/heat_tools
    bash valid_stack_integrity.sh
     if [ $? -ne 0 ]
    then
        exit 4
    fi
    echo "ERROR MUST FOLLOW"
    bash invalid_stack_integrity.sh
    if [ $? -eq 0 ]
    then
        exit 5
    fi

    go_to_dirname
    $(pwd)/heat/etcd/integrity.sh
    if [ $? -eq 0 ]
    then
        exit 6
    fi
    return 0
}

function main
{
    go_to_dirname
    alias sti="$(pwd)/script/heat_tools/stack_integrity.py"
    run_tests
}

main
exit $?