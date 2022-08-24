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

export TEST_FILES="${PROJECT_DIR:-}/test_files"
