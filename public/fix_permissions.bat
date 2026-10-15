@echo off
echo ============================================
echo  FIXING PERMISSIONS FOR MARK XLVIII
echo ============================================
echo.

:: Take ownership of the folder
echo Taking ownership...
takeown /f "C:\Users\%USERNAME%\Mark-XLVII" /r /d y >nul 2>&1

:: Reset permissions
echo Resetting permissions...
icacls "C:\Users\%USERNAME%\Mark-XLVII" /reset /t /c /q >nul 2>&1

:: Remove read-only attribute
echo Removing read-only attributes...
attrib -r -s -h "C:\Users\%USERNAME%\Mark-XLVII" /s /d >nul 2>&1

:: Delete the problematic .git folder
echo Removing locked .git folder...
if exist "C:\Users\%USERNAME%\Mark-XLVII\.git" (
    rmdir /s /q "C:\Users\%USERNAME%\Mark-XLVII\.git" 2>nul
    if errorlevel 1 (
        echo.
        echo ERROR: Could not delete .git folder
        echo Please close any programs using Mark-XLVII and try again
        echo Or delete it manually: C:\Users\%USERNAME%\Mark-XLVII\.git
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo  PERMISSIONS FIXED!
echo ============================================
echo.
echo Now run the installer again:
echo   python install_mark_xlviii.py
echo.
pause
