@echo off
REM Double-click this when a rebuild does not seem to take effect.
REM It prints everything needed to work out why. Nothing is changed.

cd /d "%~dp0"

echo ============================================================
echo  OSRI site diagnostic
echo ============================================================
echo.
echo  THIS FOLDER:
echo    %CD%
echo.
echo  Is this the folder you have been editing? If you are not
echo  certain, that is very likely the problem.
echo.

echo ------------------------------------------------------------
echo  Is the folder properly extracted?
echo ------------------------------------------------------------
if exist "build.py" (echo    build.py        found) else (echo    build.py        MISSING)
if exist "pages"    (echo    pages\          found) else (echo    pages\          MISSING)
if exist "content"  (echo    content\        found) else (echo    content\        MISSING)
if exist "css"      (echo    css\            found) else (echo    css\            MISSING)
echo.
echo  If anything says MISSING, you are working inside the zip
echo  preview instead of an extracted folder. Right-click the zip,
echo  choose "Extract All", and work in the folder it creates.
echo.

echo ------------------------------------------------------------
echo  Python
echo ------------------------------------------------------------
where python 2>nul
where py 2>nul
python --version 2>nul
echo.

echo ------------------------------------------------------------
echo  SOURCE files you edit (newest last)
echo ------------------------------------------------------------
dir /T:W /O:D /B /A:-D pages\*.html 2>nul
echo.
for %%F in (pages\*.html) do echo    %%~tF   pages\%%~nxF
echo.

echo ------------------------------------------------------------
echo  OUTPUT files the site uses
echo ------------------------------------------------------------
for %%F in (*.html) do echo    %%~tF   %%~nxF
echo.
echo  Each output file should be NEWER than the page it came from.
echo  If an output file is older, the build did not write it.
echo.

echo ------------------------------------------------------------
echo  Running the build now
echo ------------------------------------------------------------
if exist "build.py" python build.py
echo.
echo ============================================================
echo  Press any key to close.
pause >nul
