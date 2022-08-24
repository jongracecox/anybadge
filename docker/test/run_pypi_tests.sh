#!/bin/bash

source "${SOURCE_DIR:-.}/helpers.sh" || { echo "Failed to load helpers." ; exit 1 ; }

if [[ -z ${VERSION} ]] || [[ ${VERSION} = latest ]]; then
  version_str=""
else
  version_str="==$VERSION"
fi

echo -n "Installing anybadge${version_str}... "
pip install "anybadge${version_str}" > "${TEST_FILES}/pip_install.log" 2>&1
check_rc
echo "OK"

"${SOURCE_DIR:-.}/shell_tests.sh"
