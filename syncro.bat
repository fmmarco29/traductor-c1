@echo off
REM Este script sincroniza tu repositorio local con GitHub.

REM Cambiar al directorio donde está el repositorio
cd /d "%~dp0"

REM --- Hacer pull desde GitHub para traer cambios remotos ---
echo --- Haciendo pull desde GitHub...
git pull origin main

REM --- Añadir todos los archivos nuevos/modificados/eliminados ---
echo --- Añadiendo cambios al repositorio...
git add -A

REM --- Hacer commit con un mensaje automático basado en la fecha y hora ---
for /f %%a in ('wmic os get localdatetime ^| find "."') do set datetime=%%a
set timestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%
set commitmsg=Auto commit %timestamp%

echo --- Haciendo commit con mensaje: %commitmsg%
git commit -m "%commitmsg%"

REM --- Subir los cambios a GitHub ---
echo --- Subiendo cambios a GitHub...
git push origin main

echo --- ¡Listo! Los cambios han sido subidos correctamente.
pause
