import random
from datetime import datetime, timedelta

import pandas as pd
import psycopg2
from psycopg2 import OperationalError, Error


def try_connect_postgres():
    """
    Пытаемся подключиться к несуществующей БД PostgreSQL.
    """
    print("[INFO] Trying to connect to PostgreSQL...")

    try:
        conn = psycopg2.connect(
            dbname="shop",
            user="app",
            password="secret",
            host="db",      # такого хоста у нас нет, подключение упадет
            port=5432,
            connect_timeout=3
        )
        conn.close()
        print("[INFO] Connected to PostgreSQL successfully")
        return True
    except (OperationalError, Error) as e:
        print("[ERROR] Cannot connect to PostgreSQL:", e)
        print("[INFO] Database unavailable, switching to local mode")
        return False


def generate_ecommerce_data(n_orders: int = 100) -> pd.DataFrame:
    """
    Генерация синтетических данных по интернет-магазину.
    Поля:
      - order_id
      - order_date
      - amount
      - category
      - is_returned
    """
    now = datetime.now()
    categories = ["Electronics", "Clothes", "Books", "Home", "Toys"]

    rows = []
    for i in range(1, n_orders + 1):
        order_date = now - timedelta(days=random.randint(0, 30))
        amount = round(random.uniform(10, 500), 2)
        category = random.choice(categories)
        is_returned = random.choice([0, 1])  # 0 - не возврат, 1 - возврат

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


def calc_metrics(df: pd.DataFrame) -> dict:
    """
    Считаем простые метрики:
      - total_revenue: суммарная выручка
      - orders_count: количество заказов
      - returns_share_percent: доля возвратов в процентах
    """
    total_revenue = df["amount"].sum()
    orders_count = len(df)
    returns_share = df["is_returned"].mean() * 100  # 0/1 -> доля

    metrics = {
        "total_revenue": round(total_revenue, 2),
        "orders_count": int(orders_count),
        "returns_share_percent": round(returns_share, 2),
    }
    return metrics


def main():
    print("[INFO] Starting analytics service (variant 20, E-commerce Sales)")

    connected = try_connect_postgres()

    if not connected:
        print("[INFO] Working in LOCAL mode (synthetic data)")

    df = generate_ecommerce_data(n_orders=200)
    metrics = calc_metrics(df)

    print("[RESULT] E-commerce metrics:")
    for key, value in metrics.items():
        print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
