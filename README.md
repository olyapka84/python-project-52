### Hexlet tests and linter status:
[![Actions Status](https://github.com/olyapka84/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/olyapka84/python-project-52/actions)

# Task Manager (Hexlet Project 52)

Финальный проект курса Python на Хекслете — менеджер задач на Django.

## Деплой

Приложение доступно по адресу: [https://python-project-52-76f1.onrender.com/](https://python-project-52-76f1.onrender.com/)

## Локальный запуск

1. Установите зависимости из файла `requirements.txt`, который лежит в корне репозитория (`code/requirements.txt` в окружении Hexlet):

   ```bash
   pip install -r requirements.txt
   ```

2. Выполните миграции и запустите сервер разработки:

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```
