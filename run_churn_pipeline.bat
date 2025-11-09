@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem === 0) Carpeta base del proyecto (donde está este .bat) ===
set "BASE=%~dp0"
rem Quitar la barra final si existe para evitar dobles barras
if "%BASE:~-1%"=="\" set "BASE=%BASE:~0,-1%"

rem === 1) Python del venv ===
set "PY=%BASE%\.venv\Scripts\python.exe"

rem === 2) Carpeta de logs ===
set "LOGDIR=%BASE%\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

rem === 3) Timestamp seguro YYYYMMDD_HHMM (sin / ni :) ===
set "TS=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%"
rem Reemplazar espacio por 0 y quitar dos puntos, por si acaso
set "TS=%TS: =0%"
set "TS=%TS::=%"

set "LOG=%LOGDIR%\pipeline_%TS%.log"

rem === 4) Debug: imprime las rutas calculadas ===
echo BASE=%BASE%
echo PY=%PY%
echo LOG=%LOG% 
echo.

rem Validar que exista python del venv
if not exist "%PY%" (
  echo [ERROR] No encuentro el Python del venv en: "%PY%"
  exit /b 9001
)

rem === 5) Ir a la carpeta base y ejecutar el orquestador ===
pushd "%BASE%"
echo ===== INICIO %date% %time% (venv) ===== >> "%LOG%"

"%PY%" ".\src\run_pipeline.py"  >> "%LOG%" 2>&1
set "RC=%ERRORLEVEL%"

echo ===== FIN %date% %time% (rc=%RC%) ===== >> "%LOG%"
popd

exit /b %RC%
