import os
import shutil

"""
use it to refresh database
and create a superuser and a normal user
"""

if os.path.isfile('db.sqlite3'):
    os.remove('db.sqlite3')
    print("delete file 'db.sqlite3'\n")

if os.path.isdir('whoosh_index'):
    shutil.rmtree('whoosh_index')
    print("delete dir 'whoosh_index'\n")

os.system('python manage.py makemigrations')

os.system('python manage.py migrate --run-syncdb')

os.system('python manage.py rebuild_index')

os.system("echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')\" | python manage.py shell")

print("\ncreate superuser('admin','admin@example.com','pass')")

os.system("echo \"from django.contrib.auth.models import User; User(username='user-1', password='pass').save()\" | python manage.py shell")

print("\ncreate user-1 (username='user-1',password='pass')")

