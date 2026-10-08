@echo off
TITLE ERP Django - Guardando Sesion
COLOR 0E

:: --- 1. RUTAS ---
SET PC_WORK=C:\Temp_Workspace_ERP
SET USB_PATH=%~dp0
SET PATH=%USB_PATH%Git_Portable\cmd;%USB_PATH%Git_Portable\ucrt64\bin;%PATH%
git config --global --add safe.directory *

echo ==================================================
echo  ERP DJANGO :: PC ^-^> USB (RESPALDO)
echo ==================================================

:: --- 2. VERIFICAR QUE EXISTE EL TALLER ---
if not exist "%PC_WORK%" (
    echo [ERROR] No existe %PC_WORK%
    echo Ejecuta primero iniciar_sesion.bat
    pause & exit /b 1
)

cd /d "%PC_WORK%"

:: --- 3. AVISO DE CAMBIOS SIN COMMIT ---
echo.
git status --short
echo.
echo Si arriba hay archivos listados, NO estan en un commit.
echo Cierra y haz git add . y git commit antes de continuar.
echo.
pause

:: --- 4. SUBIR A GITHUB (si hay internet) ---
git push
if errorlevel 1 echo [AVISO] No se pudo hacer push. Los commits se guardaran solo en el USB.

:: --- 5. CODIGO Y ARCHIVOS AL USB (raiz, no subcarpeta) ---
echo Guardando archivos en la USB...
robocopy "%PC_WORK%" "%USB_PATH%." /E /XD .git env_erp venv __pycache__ Git_Portable Python_Portable WorkSpace_ERP "System Volume Information" /XF *.pyc >nul

:: --- 6. EL .GIT (LO MAS IMPORTANTE) ---
robocopy "%PC_WORK%\.git" "%USB_PATH%.git" /MIR >nul

echo.
echo Ultimos commits guardados en el USB:
git -C "%USB_PATH%." log --oneline -3

echo.
echo ==================================================
echo  RESPALDO COMPLETADO. Es seguro retirar la USB.
echo ==================================================
pause