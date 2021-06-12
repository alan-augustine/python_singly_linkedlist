#!/bin/bash

function loginfo() {
	echo "INFO:$(date '+%F %T'): ************************* ${1} ***************************"
}

function logerror() {
	echo "ERROR:$(date '+%F %T'): ************************* ${1} ***************************"
}

function setup() {
    set -e
    echo "Timezone = $(date  '+%Z %z')"
    kill_local_pypi_server_if_exists
    cleanup_directories
}

# cleanup is required mainly for testing in local Dev machine
# below function can be used in setup() & teardown() functions
function cleanup_directories() {
    # ./venv_dir - do not remove venv directory
    # removing & creating venv dir for each iteration of testing is inefficient

    # set +e, as below commands may return non-zero exit  code.
    # If no directory existsa, then script will exit, since we set -e 
    # in setup() function
    set +e
    [[ -d ./pypi_packages ]] && rm -Rf ./pypi_packages
    [[ -d build ]] && rm -Rf build
    [[ -d dist ]] && rm -Rf dist
    [[ -d src/singly_linkedlist.egg-info ]] && rm -Rf src/*.egg-info
    [[ -f log_pypi_server.log ]] && rm -f log_pypi_server.log
    set -e
}

function create_build_env() {
    if [[ ! -e ./venv_dir ]];then
        mkdir ./venv_dir
        loginfo "Created venv directory $PWD/venv_dir"
    fi

    # set-up vnev
    loginfo  "Activating venv"
    python3 -m venv ./venv_dir
    source  ./venv_dir/bin/activate
    pip install -r requirements.txt
    loginfo "Activated venv"

}

function kill_local_pypi_server_if_exists() {
    set +e
    existing_pypi_pid=$(pgrep pypi-server)
    set -e

    if [[ -z $existing_pypi_pid ]];then
        echo "No running Pypi server process detected"
    else
        kill -9 $existing_pypi_pid
        echo "Killed Pypi server process with PID $existing_pypi_pid"
    fi 
}

function start_local_pypi_server() {
    # setup local pypi server 
    # for package upload & download
    mkdir pypi_packages
    pypi-server -P . -a . -p 8085 pypi_packages &> log_pypi_server.log &

}

# lint
function lint() {
    loginfo "Lint - start"

    loginfo "flake8 - start"
    flake8 src/singly_linkedlist/singly_linkedlist.py || exit
    flake8 tests || exit
    loginfo "flake8 - end"

    loginfo "pylint - start"
    pylint --ignore=__pycache__ src/ || exit
    loginfo "pylint - end"

    loginfo "Lint - end"
}

# test
function test_code(){
    loginfo "Running Units Tests"
    python3 -m pytest -v --ignore=lib --ignore=venv_dir tests/
    loginfo "Unit Tests - Finished"
}

# build
function build() {
    loginfo "Build - start"
    python -m build

    # https://packaging.python.org/glossary/#term-Built-Distribution
    echo "Contents of wheel file(built distribution):"
    unzip -l dist/*whl

    # https://packaging.python.org/glossary/#term-Source-Archive
    echo "Contents of tar file(source archive):"
    tar --list -f  dist/*tar.gz

    loginfo "Build - end"

}


# Release/Upload artifacts/packages generated
function release() {
    loginfo "Release - start"
    # connection attempts to local Pypi server
    max_attempts=5
    readonly max_attempts
    attempt=1
    wait_seconds=5
    readonly wait_seconds
    while [[ $attempt -le $max_attempts ]];do 
        if nc -zv localhost 8085;then
            echo "Connection to local Pypi server succeeded, proceeding to upload artifacts"
	    break
        else
            echo "Attempt $attempt : Connection to local Pypi server failed"
	    echo "Waiting $wait_seconds seconds"
	    let attempt++
	    sleep $wait_seconds
        fi

        if [[ $attempt -eq $max_attempts ]];then
            echo "Exceeded maximum connection attempts. Aborting!"
	    exit 1
        fi
    done
    # end of while loop

    # Upload artifacts to local pypi server
    # Pypi server is started in non-auth mode, 
    # but it expects some username & password, although not used
    export TWINE_USERNAME='dummy'
    export TWINE_PASSWORD='dummy'
    twine upload  --non-interactive --repository-url http://localhost:8085 dist/*

    loginfo "Release - end"

}
# end of release() function

function install_generated_package() {
    pip install -v --index-url http://localhost:8085 singly_linkedlist
}

function import_installed_package() {
    if python -c 'import singly_linkedlist';then
        echo "Package import successfull"
    else
        echo "Package import failed"
        exit 1
    fi

}


function teardown() {
    pip uninstall -y singly_linkedlist
    cleanup_directories
    kill_local_pypi_server_if_exists

}


function main() {
    # start
    setup
    create_build_env
    start_local_pypi_server
    lint
    test_code
    build
    release
    install_generated_package
    import_installed_package
    teardown
    # end
}

# script execution starts here
main "$@"
