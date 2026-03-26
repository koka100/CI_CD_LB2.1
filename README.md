# CI_CD_LB2.1
# Лабораторная работа 02.1

**ФИО: Бойко Константин Константинович**
**Группа: АДЭУ-221**  
**Вариант: 20**   
**Тема данных:** E-commerce Sales  
**Техническое задание:** PostgreSQL Client (обработка ошибки подключения, переход в локальный режим)


## 1. Описание задачи

Цель работы — разработать аналитический Python-скрипт для предметной области E-commerce Sales и упаковать его в Docker-образ.  
Скрипт при запуске пытается подключиться к несуществующей базе данных PostgreSQL, обрабатывает ошибку подключения (try-except) и переходит в "локальный режим".  
В локальном режиме данные о заказах генерируются синтетически, после чего рассчитываются бизнес-метрики:

- суммарная выручка (total_revenue);
- количество заказов (orders_count);
- доля возвратов в процентах (returns_share_percent).

## Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]


## Генерация данных
def generate_ecommerce_data(n_orders: int = 100) -> pd.DataFrame:
    now = datetime.now()
    categories = ["Electronics", "Clothes", "Books", "Home", "Toys"]

    rows = []
    for i in range(1, n_orders + 1):
        order_date = now - timedelta(days=random.randint(0, 30))
        amount = round(random.uniform(10, 500), 2)
        category = random.choice(categories)
        is_returned = random.choice()[11]

        rows.append(
            {
                "order_id": i,
                "order_date": order_date,
                "amount": amount,
                "category": category,
                "is_returned": is_returned,
            }
        )

    df = pd.DataFrame(rows)
    return df


## Расчет метрик

def calc_metrics(df: pd.DataFrame) -> dict:
    total_revenue = df["amount"].sum()
    orders_count = len(df)
    returns_share = df["is_returned"].mean() * 100

    metrics = {
        "total_revenue": round(total_revenue, 2),
        "orders_count": int(orders_count),
        "returns_share_percent": round(returns_share, 2),
    }
    return metrics





## Настройка директорий проекта
<img width="668" height="366" alt="image" src="https://github.com/user-attachments/assets/36907d46-81b9-446d-9b63-6b93c8efc949" />

## Сборка образа
<img width="732" height="541" alt="image" src="https://github.com/user-attachments/assets/1cc58a14-7598-4fcf-bbf8-967a8ef8b833" />

## Попытка подключения к PostgreSQL и обработка ошибки
<img width="731" height="242" alt="image" src="https://github.com/user-attachments/assets/3dd353f1-6f49-4633-b63b-6a9dd278f8f3" />

