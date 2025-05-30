@echo off
setlocal

REM Installer PyInstaller et requests si besoin
python -m pip install --upgrade pip
python -m pip install requests pyinstaller

REM Dossier de sortie pour les exécutables
set OUTPUT_DIR=%TEMP%\build_output
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Assumer que les scripts Python sont dans %TEMP% (ou adapter)
REM Ici on va copier les scripts depuis %TEMP% vers %TEMP%\build_temp pour compiler proprement

set TEMP_BUILD=%TEMP%\build_temp
if exist "%TEMP_BUILD%" rd /s /q "%TEMP_BUILD%"
mkdir "%TEMP_BUILD%"

REM Copier les scripts Python dans build_temp
copy "%TEMP%\update_script.py" "%TEMP_BUILD%"
copy "%TEMP%\update_script2.py" "%TEMP_BUILD%"

pushd "%TEMP_BUILD%"

echo [*] Compilation de update_script.py ...
pyinstaller --noconfirm --onefile --windowed --distpath "%OUTPUT_DIR%" "update_script.py"
if errorlevel 1 (
    echo [!] Erreur lors de la compilation de update_script.py
    pause
    exit /b 1
)

echo [*] Compilation de update_script2.py ...
pyinstaller --noconfirm --onefile --windowed --distpath "%OUTPUT_DIR%" "update_script2.py"
if errorlevel 1 (
    echo [!] Erreur lors de la compilation de update_script2.py
    pause
    exit /b 1
)

popd

echo [✓] Compilation terminée. Les exe sont dans %OUTPUT_DIR%
timeout /t 3 /nobreak >nul
exit /b 0
