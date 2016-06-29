@echo off
echo ************************************
echo * You are about to register package
echo ************************************
echo Press ctrl+C to interrupt or...
pause
twine register -r pypi --config-file .pypirc dist/pyisql-0.1.1.zip
pause
