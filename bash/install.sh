#!/bin/sh

cd ..

# Create the directory for your application
if [ ! -d "/usr/local/jobseeker" ]; then
    sudo mkdir /usr/local/jobseeker
fi

# Copy the binary file to the new directory
sudo cp jobseeker /usr/local/jobseeker/jobseeker
# Copy the geckodriver to the new directory
sudo cp geckodriver /usr/local/jobseeker/geckodriver
sudo cp icon.png /usr/local/jobseeker/icon.png

# Copy the desktop file to the system's applications directory
sudo cp bash/jobseeker.desktop /usr/share/applications/jobseeker.desktop

# Make the desktop file readable and executable
sudo chmod +x /usr/share/applications/jobseeker.desktop
sudo chmod +x /usr/local/jobseeker/jobseeker

echo "Installed Job Seeker Application."