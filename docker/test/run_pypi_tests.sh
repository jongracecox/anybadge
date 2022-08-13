#!/bin/bash

error() {
  echo "==============================================================================="
  echo " An error was encountered."
  echo "==============================================================================="
  }

check_rc() {
  if [[ $? -ne 0 ]]; then
    error
    exit 1
  fi
  }

TEST_FILES="/test_files"

if [[ -z {$VERSION} ]] || [[ ${VERSION} = latest ]]; then
  version_str=""
else
  version_str="==$VERSION"
fi

echo -n "Installing anybadge${version_str}... "
pip install anybadge${version_str} > "${TEST_FILES}/pip_install.log" 2>&1
check_rc
echo "OK"

installed_version=$(pip freeze | grep -e "^anybadge==" | sed 's/^.*==//' )
datestamp=$(date '+%Y-%m-%d_%H%M%S')

TEST_FILES="${TEST_FILES}/${installed_version}_${datestamp}"
echo -n "Creating test directory: ${TEST_FILES} "
mkdir -p ${TEST_FILES}
check_rc
echo "OK"

# Command line tests
anybadge --help > "${TEST_FILES}/test_help_text.txt" && check_rc
anybadge --label="Label" --value="Value" --file "${TEST_FILES}/test_command_line.svg" && check_rc

# Python tests
python > "${TEST_FILES}/test_python_console.log" <<EOF
import anybadge

badge = anybadge.Badge(label="Label", value="Value")
badge.write_badge(file_path="${TEST_FILES}/test_python_1.svg")
print(badge)
EOF
check_rc

# Start server
echo -n "Starting server... "
anybadge-server > "${TEST_FILES}/server_start.log" 2>&1 &
server_pid=$!
echo "OK - Started server with pid ${server_pid}"
sleep 1

kill -0 ${server_pid}
check_rc

# Test server
echo -n "Testing server badge... "
curl "http://localhost:8000/?label=Project%20Awesomeness&value=110%" -o "${TEST_FILES}/test_server.svg" --silent
check_rc
echo "OK"

echo -n "Testing server index page... "
curl "http://localhost:8000" -o "${TEST_FILES}/test_server_index.html" --silent
check_rc
echo "OK"

# Stop server
echo -n "Stopping server... "
kill $server_pid
check_rc

echo "OK"
