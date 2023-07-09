#!/bin/bash
# installs using pyinstaller

pyinstaller --onefile --name=jobseeker  --clean --distpath=. src/main.py
