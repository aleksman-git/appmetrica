# get_appmetrica.py
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import TOKEN, APP_ID, STATS_API_URL

# Даты для запроса статистики
date_to = datetime.now().strftime("%Y-%m-%d")
date_from = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

headers = {
    "Authorization": f"OAuth {TOKEN}",
    "Content-Type": "application/json"
}

# Параметры для запроса статистики по пользователям
params_users = {
    "id": APP_ID,
    "date_from": date_from,
    "date_to": date_to,
    "metrics": "ym:u:users",
    "dimensions": "ym:u:date",
    "group": "day"
}

def get_appmetrica_stats(params):
    try:
        response = requests.get(STATS_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            stats_data = response.json()
            return stats_data.get("data", [])
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

def stats_to_dataframe(stats_data):
    if not stats_data:
        # Создаём пустой DataFrame с колонками и нулевыми значениями
        dates_range = pd.date_range(start=date_from, end=date_to)
        empty_data = {"ym:u:date": dates_range.strftime("%Y-%m-%d"), "ym:u:users": [0] * len(dates_range)}
        return pd.DataFrame(empty_data)
    return pd.DataFrame(stats_data)

def save_dataframe_to_csv(df, filename="appmetrica_users.csv"):
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Данные успешно сохранены в {filename}")

if __name__ == "__main__":
    # Получаем статистику по пользователям
    users_data = get_appmetrica_stats(params_users)
    df_users = stats_to_dataframe(users_data)
    save_dataframe_to_csv(df_users, "appmetrica_users.csv")
