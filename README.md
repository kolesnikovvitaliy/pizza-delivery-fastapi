# Pizza-Delivery-Fastapi проект api магазина по продаже пиццы 
#
### Используемые технологии    
* Python3.12
* Asyncio
* FastApi
* SQLAlchemy["asyncio"]
* PostgreSql
* asyncpg
* aiosqlite
* Alembic
* Pydantic
* Docker-compose

<div class="img-div">
  <img src="https://github.com/kolesnikovvitaliy/pizza_delivery_fastapi/blob/main/docs/img/scrin_1.png" width="800"/>
</div>

## Для запуска проекта необходимо установить Poetry
```bash
pip install poetry
```

#### После установки, копировать проект на свой компьютер
##### Логи приложения расположены в директории "logs"  
```bash
git clone https://github.com/kolesnikovvitaliy/pizza-delivery-fastapi.git
```
#### Перейти в директорию pizza-delivery-fastapi/src/backend
```bash
cd pizza-delivery-fastapi/src/backend
```
#### Создать виртуальное окружение 
```bash
poetry install
```
#### Активировать виртуальное окружение
```bash
source .venv/bin/activate
```
### Запустить миграции для базы данных.
#### Если не установленна PostgreSql то запуститься встроенная Sqlite, изменений не требуется
##### Если PostgreSql установленна нужно перейти в директорию и внести изменения в файл  "environments.py"
```bash
cd backend_config
```
##### Закомментировать переменную  DB_URL_REAL и раскомментировать переменную POSTGRES_HOST 
```python
if os.path.exists(dotenv_path):
    # DB_URL_REAL: str = "sqlite+aiosqlite:///sqlite.db"  # activated if local db sqlite
    POSTGRES_HOST: str = os.environ.get("POSTGRES_LOCAL")  # activated if local db postgres
```
##### Вернуться в директорию "backend"
```bash
cd ..
```
##### Выполнить по очереди команды миграции
```bash
alembic revision --autogenerate -m "init revision alembic"
alembic upgrade head
```

### Запустить проект
```bash
poetry run python main.py
```
#### Перейдите на страницу API приложения по продаже пиццы:
```bash
http://localhost:8000/docs
```
## Запуск проекта с помощью Docker-compose

#### Все логи расположены в директории  
```bash
.docker_data
```

#### Копировать проект на свой компьютер
```bash
git clone https://github.com/kolesnikovvitaliy/pizza-delivery-fastapi.git
```
#### Перейти в директорию pizza-delivery-fastapi
```bash
cd pizza-delivery-fastapi
```
#### Сделать файлы start_dev.sh и stop_dev.sh исполняемыми
```bash
chmod +x start_dev.sh stop_dev.sh
```
#### Запустить проект
```bash
./start_dev.sh
```
#### Остановить проект
```bash
./stop_dev.sh
```
#### Перейдите по ссылке:
```bash
http://localhost:8000/docs - API
http://localhost:5050 pgAdmin 
```
##### Для входа в pgAdmin нужно:
##### Ввести пароль 'admin' и создать новый сервер:
##### General:
* name: backend
##### Connection:
* host_name: postgresql_db
* port: 5432
* db_name: backend 
* user: admin
* password: admin
##### Save
