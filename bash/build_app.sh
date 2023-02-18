#!/bin/bash
# installs using pyinstaller

cd ..

pyinstaller --onefile --name=jobseeker  --clean --distpath=. src/main.py