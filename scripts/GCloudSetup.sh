#!/bin/bash
if echo "" | gcloud auth application-default print-access-token &> /dev/null; then
    echo "gcloud already logged in"
    exit 0
else
    echo "Signing in to Google Cloud..."
fi

if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" != "debian" && "$ID" != "ubuntu" ]]; then
        echo "This script is only intended for Debian/Ubuntu distributions."
        echo "Your distribution is $ID."
        exit 1
    fi
else
    echo "The /etc/os-release file was not found. Cannot determine distribution."
    exit 1
fi

is_package_installed() {
  local package_name="$1"
  if dpkg-query -W --showformat='${Status}\n' "$package_name" 2>/dev/null | grep -q "install ok installed"; then
    return 0
  else
    return 1
  fi
}

echo "Installing dependencies..."
sudo apt-get update
is_package_installed "apt-transport-https" || sudo apt-get install apt-transport-https
if [ $? -eq 1 ]; then
    echo "apt-transport-https failed to install"
    exit 1
fi

is_package_installed "ca-certificates" || sudo apt-get install ca-certificates
if [ $? -eq 1 ]; then
    echo "ca-certificates failed to install"
    exit 1
fi

is_package_installed "gnupg" || sudo apt-get install gnupg
    if [ $? -eq 1 ]; then
        echo "gnupg failed to install"
        exit 1
    fi

is_package_installed "curl" || sudo apt-get install curl
    if [ $? -eq 1 ]; then
        echo "curl failed to install"
        exit 1
    fi

echo "Getting the key..."
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
if [ $? -eq 0 ]; then
    echo "Key was added to /usr/share/keyrings/cloud.google.gpg"
else
    echo "Key failed to add to /usr/share/keyrings/cloud.google.gpg"
    exit 1
fi

echo "Adding the repository..."
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
if [ $? -eq 0 ]; then
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main was added to /etc/apt/sources.list.d/google-cloud-sdk.list"
else
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main failed to add to /etc/apt/sources.list.d/google-cloud-sdk.list"
    exit 1
fi

echo "Installing the google-cloud-cli package..."
is_package_installed "google-cloud-cli" || sudo apt-get install google-cloud-cli
if [ $? -eq 0 ]; then
    echo "google-cloud-cli was installed successfully"
else
    echo "google-cloud-cli failed to install"
    exit 1
fi

echo "Signing in to Google Cloud..."
gcloud auth application-default login
