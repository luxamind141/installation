@echo off
setlocal

REM Installer PyInstaller et requests si besoin
python -m pip install --upgrade pip
python -m pip install requests pyinstaller

REM Création du dossier de sortie
set OUTPUT_DIR=%~dp0build_output
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Compiler update_script.py
echo [*] Compilation de update_script.py ...
pyinstaller --noconfirm --onefile --windowed --distpath "%OUTPUT_DIR%" "%~dp0update_script.py"
if errorlevel 1 (
    echo [!] Erreur lors de la compilation de update_script.py
    pause
    exit /b 1
)

REM Compiler un second script exemple, remplace update_script2.py par ton script réel
echo [*] Compilation de update_script2.py ...
pyinstaller --noconfirm --onefile --windowed --distpath "%OUTPUT_DIR%" "%~dp0update_script2.py"
if errorlevel 1 (
    echo [!] Erreur lors de la compilation de update_script2.py
    pause
    exit /b 1
)

echo [✓] Compilation terminée. Les exe sont dans %OUTPUT_DIR%
pause
endlocal
