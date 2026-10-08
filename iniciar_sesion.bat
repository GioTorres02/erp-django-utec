@echo off
TITLE ERP Django - Iniciando Sesion
COLOR 0A

:: -- 1. RUTAS DINAMICAS --
SET USB_PATH=%~dp0
SET PC_WORK=C:\Temp_Workspace_ERP

echo ======================================================
echo  ERP DJANGO :: USB ^-^> PC
echo  USB: %USB_PATH%
echo  PC:  %PC_WORK%
echo ======================================================

:: -- 2. CREAR TALLER EN DISCO LOCAL --
if not exist "%PC_WORK%" (
    mkdir "%PC_WORK%"
    echo [OK] Carpeta creada: %PC_WORK%
)

:: -- 3. PATH TEMPORAL (antes de usar git) --
SET PATH=%USB_PATH%Python_Portable;%USB_PATH%Python_Portable\Scripts;%USB_PATH%Git_Portable\cmd;%USB_PATH%Git_Portable\ucrt64\bin;%PATH%
git config --global --add safe.directory *

:: -- 4. SINCRONIZAR USB -> PC (raiz del USB, sin pisar archivos mas nuevos) --
echo Sincronizando proyecto a la PC...
robocopy "%USB_PATH%." "%PC_WORK%" /E /XO /XD .git env_erp venv __pycache__ Git_Portable Python_Portable WorkSpace_ERP git_respaldo_hoy "System Volume Information" $RECYCLE.BIN /XF *.pyc >nul

:: -- 5. TRAER EL .GIT (solo si la PC aun no tiene uno) --
if not exist "%PC_WORK%\.git" (
    robocopy "%USB_PATH%.git" "%PC_WORK%\.git" /E >nul
    git -C "%PC_WORK%" config --unset core.worktree
    echo [OK] Repositorio git copiado a la PC.
)
echo [OK] Sincronizacion completada.

:: -- 6. RECREAR ENTORNO VIRTUAL SI NO EXISTE EN PC --
if not exist "%PC_WORK%\env_erp" (
    echo Creando entorno virtual en la PC...
    python -m virtualenv "%PC_WORK%\env_erp"
    if exist "%PC_WORK%\requirements.txt" (
        echo Instalando dependencias desde requirements.txt...
        "%PC_WORK%\env_erp\Scripts\python.exe" -m pip install -r "%PC_WORK%\requirements.txt" --quiet
    )
    echo [OK] Entorno virtual creado.
)

:: -- 7. ACTIVAR ENTORNO VIRTUAL --
SET PATH=%PC_WORK%\env_erp\Scripts;%PATH%
echo [OK] Entorno virtual activo.

:: -- 8. IR A LA CARPETA DE TRABAJO --
cd /d "%PC_WORK%"
echo.
echo VERSIONES ACTIVAS:
python --version
git --version
echo.
echo --- RECUERDA EJECUTAR finalizar_sesion.bat AL TERMINAR ---
cmd /k "echo ERP listo en %PC_WORK%"