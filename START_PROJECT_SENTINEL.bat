@echo off
echo ================================================================
echo    PROJECT SENTINEL - Real-Time Retail Intelligence System
echo                   Team: Bit-Busters
echo ================================================================
echo.

cd /d "%~dp0"

echo Starting Project Sentinel with synchronized dashboards...
echo.

python launch_synchronized_system.py

pause