# Volunteer Management

Веб-приложение на Django для управления волонтерскими проектами, организациями, новостями и заявками волонтеров.

## Что нужно установить

- Python 3.11+ или 3.12+
- Git
- PostgreSQL, если хотите подключить внешнюю базу данных

По умолчанию проект может запускаться на локальной SQLite-базе, поэтому PostgreSQL для первого запуска не обязателен.

## Как скачать проект

```bash
git clone https://github.com/Arlan010/volunteer_management.git
cd volunteer_management
```

## Как создать виртуальное окружение

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

## Как установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Как настроить базу данных

Для обычного локального запуска ничего дополнительно настраивать не нужно: проект использует `db.sqlite3`.

Если нужна PostgreSQL-база, создайте файл `.env` в корне проекта и добавьте туда строку подключения:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB_NAME?sslmode=require
```

Файл `.env` не нужно загружать на GitHub, потому что в нем могут быть пароли и секретные данные.

## Как применить миграции

```bash
python manage.py migrate
```

## Как создать администратора

```bash
python manage.py createsuperuser
```

После команды Django попросит ввести логин, email и пароль.

Если администратор уже есть, но пароль забыт, пароль можно поменять так:

```bash
python manage.py changepassword USERNAME
```

## Как запустить проект

```bash
python manage.py runserver
```

После запуска сайт будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

Админ-панель:

```text
http://127.0.0.1:8000/ru/admin/
```

или:

```text
http://127.0.0.1:8000/kk/admin/
```

## Полезные команды для разработки

Создать миграции после изменения моделей:

```bash
python manage.py makemigrations
```

Применить миграции:

```bash
python manage.py migrate
```

Собрать статические файлы для деплоя:

```bash
python manage.py collectstatic
```

## Как загрузить изменения на GitHub

Проверить измененные файлы:

```bash
git status
```

Добавить файлы в коммит:

```bash
git add .
```

Создать коммит:

```bash
git commit -m "Update project state and setup instructions"
```

Отправить изменения на GitHub:

```bash
git push origin main
```

