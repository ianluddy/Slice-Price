python setup.py bdist_egg --exclude-source-files
rmdir /s /q build
rmdir /s /q slice_scanner.egg-info
cd dist
move slice* ..
cd ..
rmdir /s /q dist