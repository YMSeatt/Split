#!/usr/bin/env sh

set -e

# This is a simplified gradlew script. A real one is much more complex.
# This might not work depending on the environment's capabilities.

echo "Attempting to run Gradle..."

# Try to find a system-installed gradle
if command -v gradle >/dev/null 2>&1; then
  echo "Found system Gradle. Using it."
  gradle "$@"
  exit $?
fi

echo "System Gradle not found. This script cannot download the wrapper."
echo "Please install Gradle or provide a full gradlew script."
exit 1
