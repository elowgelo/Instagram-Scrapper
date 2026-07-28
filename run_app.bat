@echo off
title "Instagram Scraper & Keyword Filter Engine"
echo ===================================================================
echo 📸 INSTAGRAM SCRAPER & KEYWORD FILTER ENGINE (DESKTOP EDITION)
echo ===================================================================
echo Memeriksa dan membersihkan port server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
echo Menyalakan server aplikasi di laptop Anda...
echo.
python launcher.py
pause
