#!/bin/sh

if [ -d "/usr/local/jobseeker" ]; then
    rm -r /usr/local/jobseeker
    rm /usr/share/applications/jobseeker.desktop
fi

echo "Uninstalled Job Seeker Application."