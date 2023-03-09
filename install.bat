@echo off
title Install requirement

echo          o
echo           o
echo         ___
echo         ^| ^|           Starting install necessary
echo         ^| ^|
echo         ^|o^|           packages...
echo        .' '.
echo       /  o  \         Wait for a second ...
echo      :____o__:
echo      '._____.'
@REM echo. is to create blank line
echo. 
echo                       Press any key to confirm install
pause >nul
echo.
@pip install -r requirement.txt
echo.

cls
echo          o
echo           o
echo         ___
echo         ^| ^|           Installing has finished, ready to use!
echo         ^| ^|
echo         ^|o^|           Press any key to exit!
echo        .' '.
echo       /  o  \         
echo      :____o__:
echo      '._____.'

echo.
pause >nul