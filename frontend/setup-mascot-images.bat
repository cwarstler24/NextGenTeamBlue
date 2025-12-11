@echo off
echo ========================================
echo Team Blue Mascot Image Setup
echo ========================================
echo.
echo Please save your 3 mascot images to:
echo %CD%\public\mascot\
echo.
echo Required filenames:
echo   1. mascot-hero.png      (Helicopter rescue scene)
echo   2. mascot-action.png    (Jungle/explosions scene)
echo   3. mascot-portrait.png  (Alternative pose)
echo.
echo After saving the images, your theme will be complete!
echo.
echo Press any key to open the mascot folder...
pause > nul
start "" "%CD%\public\mascot"
