@echo off
REM ============================================
REM Ghana Real Estate - Push to GitHub Script
REM ============================================

echo.
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% equ 0 (
    echo [1] Git found! Running git commands...
    echo.
    
    git init
    git add .
    git commit -m "Initial commit: Ghana Real Estate Premium Odoo Module"
    git remote add origin https://github.com/nyoikepaul/ghana_real_estate.git
    git branch -M main
    git push -u origin main
    
    echo.
    echo ========================================
    echo DONE! Check your GitHub repository:
    echo https://github.com/nyoikepaul/ghana_real_estate
    echo ========================================
) else (
    echo [WARNING] Git is not installed on your system.
    echo.
    echo Please choose an option:
    echo.
    echo Option A: Install Git and run this script again
    echo   1. Download Git: https://git-scm.com/download/win
    echo   2. Install Git (use default settings)
    echo   3. Run this script again
    echo.
    echo Option B: Upload files manually via GitHub web
    echo   1. Go to: https://github.com/new
    echo   2. Repository name: ghana_real_estate
    echo   3. Select "Public" or "Private"
    echo   4. Click "Create repository"
    echo   5. Click "uploading an existing file"
    echo   6. Drag all files from this folder and drop
    echo   7. Click "Commit changes"
    echo.
    echo Your files are ready at:
    echo %cd%
    echo.
)

pause
