## Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/GeraPegov/tgbot_newsletter
cd tgbot_newsletter
```

### 2. Создайте виртуальное окружение
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash 
pip install -r requirements.txt
```

### 4. Настройте переменные окружения
```bash
cp .env.example .env
```

## Настройка базы данных

### 1. Запустите сервер PostgreSQL 


### 2. Создайте бд и таблицы
```bash 
python scripts/init_db.py
python scripts/init_table.py
```


### Запуск тестов
```bash
pytest
```

## Запуск приложения
Убедитесь что вы в директории проекта
```bash
python main.py
```