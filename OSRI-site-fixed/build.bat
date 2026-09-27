@echo off
REM Double-click this file to rebuild the site.
REM It moves to its own folder first, so it works from anywhere.

cd /d "%~dp0"

echo ============================================================
echo  Building the OSRI site
echo ============================================================
echo.
echo  Folder: %CD%
echo.
echo  ^(If that is not the folder you just edited, you have two
echo   copies of the site and are editing the wrong one.^)
echo.

if not exist "build.py" goto nobuildfile
if not exist "pages" goto nopages

set "PY="
where python >nul 2>nul
if not errorlevel 1 set "PY=python"
if defined PY goto run
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if defined PY goto run
goto nopython

:run
%PY% build.py
if errorlevel 1 goto failed
goto done

:failed
echo.
echo ============================================================
echo  BUILD FAILED - the .html files were NOT updated.
echo  Read the message above: it names the file and the problem.
echo ============================================================
goto done

:nobuildfile
echo  ERROR: build.py is not in this folder.
echo  You are running build.bat from the wrong place, or the
echo  folder was not fully extracted from the zip.
goto done

:nopages
echo  ERROR: there is no "pages" folder here.
echo  The site folder was not fully extracted from the zip.
goto done

:nopython
echo  Python was not found.
echo.
echo  Install it from python.org/downloads and tick
echo  "Add python.exe to PATH" on the first installer screen.
goto done

:done
echo.
echo  Press any key to close this window.
pause >nul
