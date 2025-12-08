@echo off
REM Deployment script for Vibe Hub (Windows)
REM This script helps automate common deployment tasks

echo ===================================
echo Vibe Hub Deployment Helper
echo ===================================
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo WARNING: Virtual environment not activated!
    echo Please activate it first:
    echo   vibe-hub-mvp\Scripts\activate
    pause
    exit /b 1
)

echo Virtual environment detected: %VIRTUAL_ENV%
echo.

:menu
echo Select deployment task:
echo 1) Run migrations
echo 2) Collect static files
echo 3) Run tests
echo 4) Create superuser
echo 5) Full deployment (migrations + static + tests)
echo 6) Initial setup (migrations + static + superuser)
echo 7) Exit
echo.

set /p choice="Enter choice [1-7]: "

if "%choice%"=="1" goto migrations
if "%choice%"=="2" goto static
if "%choice%"=="3" goto tests
if "%choice%"=="4" goto superuser
if "%choice%"=="5" goto full
if "%choice%"=="6" goto initial
if "%choice%"=="7" goto end
goto invalid

:migrations
echo Running database migrations...
python manage.py migrate
if errorlevel 1 goto error
echo Migrations complete
echo.
goto end

:static
echo Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 goto error
echo Static files collected
echo.
goto end

:tests
echo Running test suite...
python manage.py test
if errorlevel 1 goto error
echo Tests passed
echo.
goto end

:superuser
echo Creating superuser...
python manage.py createsuperuser
if errorlevel 1 goto error
echo Superuser created
echo.
goto end

:full
echo Running full deployment...
echo.
echo Running tests...
python manage.py test
if errorlevel 1 goto error
echo.
echo Running migrations...
python manage.py migrate
if errorlevel 1 goto error
echo.
echo Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 goto error
echo.
echo ===================================
echo Full deployment complete!
echo ===================================
echo.
echo Next steps:
echo 1. Restart your web server
echo 2. Check application logs
goto end

:initial
echo Running initial setup...
echo.
echo Running migrations...
python manage.py migrate
if errorlevel 1 goto error
echo.
echo Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 goto error
echo.
echo Creating superuser...
python manage.py createsuperuser
if errorlevel 1 goto error
echo.
echo ===================================
echo Initial setup complete!
echo ===================================
echo.
echo Next steps:
echo 1. Start development server: python manage.py runserver
echo 2. Access admin at http://localhost:8000/admin
goto end

:invalid
echo Invalid choice. Please try again.
echo.
goto menu

:error
echo.
echo ERROR: Command failed!
pause
exit /b 1

:end
echo.
pause
