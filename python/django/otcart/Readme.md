# OTCART 
A PYTHON DJANGO Shopping cart and Template

1. Create a Python Virtual Environment
cd to development folder/path
- python3 -m venv django 
- cd django 
2. Activate env source bin/activate
3. Install Pip
-  pip install --upgrade pip  
4. Install Django admin
 python3 -m venv django   
5. create django project
-django-admin startproject otcart
6. Make Migrations and Migrate
python manage.py makemigrations && python manage.py migrate
7. Start django project server
python manage.py runserver
8. create store app
-python manage.py startapp store

9. Add SCSS FILE USage

-pip install libsass django-compressor django-sass-processor
