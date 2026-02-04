@echo off
echo Activation de l'environnement virtuel...
call .\venv\Scripts\activate.bat

echo Lancement du serveur Django...
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

pause
