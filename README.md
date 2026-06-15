# Volunteer Management

Веб-приложение на Django для управления волонтерскими проектами, организациями, новостями и заявками волонтеров.

## Стек

- Python 3.11+
- Django 5.2
- PostgreSQL через `DATABASE_URL`
- Tailwind CSS и DaisyUI через CDN
- Leaflet.js и OpenStreetMap для карты проектов
- `django-parler`, `django-rosetta`, `django-widget-tweaks`, `Pillow`

## Установка

```bash
git clone https://github.com/Arlan010/volunteer_management.git
cd volunteer_management
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Настройка базы данных

Проект использует PostgreSQL. Создайте файл `.env` в корне проекта и добавьте строку подключения:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB_NAME?sslmode=require
```

Файл `.env` не нужно загружать на GitHub.

## Команды

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

Админ-панель:

```text
http://127.0.0.1:8000/ru/admin/
```

Проверка проекта:

```bash
python manage.py check
python manage.py test
```
