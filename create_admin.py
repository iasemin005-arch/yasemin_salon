import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yasemin_salon.settings')
django.setup()

from django.contrib.auth.models import User

# Создаем суперпользователя
username = 'admin'
email = 'admin@salon.com'
password = 'Admin123456'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Суперпользователь создан!')
    print(f'Логин: {username}')
    print(f'Пароль: {password}')
else:
    print('⚠️ Суперпользователь уже существует')
