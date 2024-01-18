# Pizza-Delivery-Fastapi проект api магазина по продаже пиццы 
#
### Используемые технологиии  
* Python3.12
* Asyncio
* FastApi
* SQLAlchemy
* PostgreSql
* Alembic
* Pydantic
* Docker-compose


## Для запуска проеката необходимо установить Poetry
```bash
pip install poetry
```

#### После установки, копировать проект на свой компьютер
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
#### Запустить проект
```bash
poetry run python main.py
```
## Запуск проеката с помощью Docker-compose

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
http://localhost:8000/docs
```
