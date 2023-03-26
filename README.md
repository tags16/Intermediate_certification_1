#### Intermediate_certification_1
###### Требования
```
Python >= 3.8
python-venv >= 3.8
PostgreSQL >= 13
```

###### Сруктура проекта
- `main.py` - основной файл программы
- `.env` - базовые параметры проекта

###### Файл конфигурации `.env`
```
# Настройки подключения к БД
PG_HOST = "localhost"
PG_PORT='5432'
PG_USER = "tags16"
PG_PSWD = "**********"
PG_DB = "postgres"

# Настройка расчета ранга
PRICE=0.0001
RAM=3
SCREEN=1
CORE=2
```

###### Установка и запуск `Intermediate_certification_1`
1. Выполнить для скачивания проекта: `gh repo clone tags16/Intermediate_certification_1`
2. Создать окружение: `python -m venv venv`
3. Активировать окружение: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Запустить проект `python main.py`
- Для остановки программы нажать: `ctrl + c`
- Деактивировать окружение: `deactivate`

###### Примечание
После запуска программы: 
- создаться таблица `ic1`
- выполнится парсинг ноутбуков
- заполнится таблица
- результат с топом ноутбуков (файл `result-ic-1.csv`)
