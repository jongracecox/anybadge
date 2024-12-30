#!/bin/bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

echo "Running shell tests..."
echo "Source directory: ${SOURCE_DIR}"
echo "Project directory: ${PROJECT_DIR}"

source "${SOURCE_DIR:-.}/helpers.sh" || { echo "Failed to load helpers." ; exit 1 ; }

echo -n "Getting installed version... "

# Get installed version
installed_version=$(pip freeze | grep -e "^anybadge==" | sed 's/^.*==//' )

if [[ -z ${installed_version} ]]; then
  installed_version=$(anybadge --version)
fi

echo "OK"
echo "Installed version: ${installed_version}"

# Create test directory
datestamp=$(date '+%Y-%m-%d_%H%M%S')

TEST_FILES="${TEST_FILES}/${installed_version}_${datestamp}"
echo -n "Creating test directory: ${TEST_FILES} "
mkdir -p ${TEST_FILES}
check_rc
echo "OK"

# Command line tests
echo -n "Testing --help... "
anybadge --help > "${TEST_FILES}/test_help_text.txt"
check_rc
echo "OK"

echo -n "Testing basic call... "
anybadge --label="Label" --value="Value" --file "${TEST_FILES}/test_command_line.svg"
check_rc
echo "OK"

echo -n "Testing with no label..."
anybadge --value="Value" --file "${TEST_FILES}/test_command_line_no_label.svg"
check_rc
echo "OK"

echo -n "Testing with no value..."
anybadge --label="Label" --file "${TEST_FILES}/test_command_line_no_value.svg"
check_rc
echo "OK"

echo -n "Testing python -m call... "
python -m anybadge --label="Label" --value="Value" --file "${TEST_FILES}/test_m_command_line.svg"
check_rc
echo "OK"

# Python tests
echo -n "Testing python api call... "
python > "${TEST_FILES}/test_python_console.log" <<EOF
import anybadge

badge = anybadge.Badge(label="Label", value="Value")
badge.write_badge(file_path="${TEST_FILES}/test_python_1.svg")
print(badge)
EOF
check_rc
echo "OK"

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
