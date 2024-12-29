"""
Модуль для получения данных о криптовалютах с использованием API CoinGecko.

Этот модуль предоставляет функциональность для получения списка поддерживаемых криптовалют
и данных о рыночных графиках, включая даты и цены за определенный период.
"""
import requests
from typing import List, Tuple
from .exceptions import APIError, DataValidationError
from .validation import validate_non_empty_list


class DataFetcher:
    """
    Класс для получения данных о криптовалютах с API CoinGecko.
    """
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def fetch_supported_assets() -> List[str]:
        """
        Получает список поддерживаемых криптовалют с помощью API.

        :return: Список идентификаторов криптовалют.
        :raises APIError: Если запрос завершился ошибкой.
        :raises DataValidationError: Если данные имеют некорректный формат.
        """
        url = f"{DataFetcher.BASE_URL}/coins/list"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise APIError(f"Ошибка API: статус {response.status_code}")

            data = response.json()

            # Валидация данных: проверяем, что список не пустой
            validate_non_empty_list(data, "Получен пустой список криптовалют.")

            # Фильтрация корректных идентификаторов криптовалют
            return [item['id'] for item in data if isinstance(item, dict) and 'id' in item]

        except requests.RequestException as e:
            raise APIError(f"Ошибка сети: {e}")
        except ValueError as e:
            raise DataValidationError(f"Ошибка обработки данных API: {e}")

    @staticmethod
    def fetch_market_chart(crypto_id: str, days: int) -> Tuple[List[str], List[float]]:
        """
        Получает данные о ценах криптовалюты за определенный период.

        :param crypto_id: ID криптовалюты (например, 'bitcoin').
        :param days: Количество дней для анализа (например, 30).
        :return: Кортеж списков с датами и ценами.
        :raises: APIError, DataValidationError
        """
        url = f"{DataFetcher.BASE_URL}/coins/{crypto_id}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                raise APIError(f"Ошибка API: статус {response.status_code}")
        except requests.RequestException as e:
            raise APIError(f"Ошибка запроса: {e}")

        try:
            data = response.json()
        except ValueError:
            raise DataValidationError("Ответ API не является корректным JSON")

        # Проверяем наличие ключа "prices" в данных
        if "prices" not in data:
            raise DataValidationError("Неверный формат данных API")

        # Извлекаем даты и цены из данных API
        dates = [item[0] for item in data["prices"]]
        prices = [item[1] for item in data["prices"]]

        # Валидация данных: списки дат и цен не должны быть пустыми
        validate_non_empty_list(dates, "Список дат пустой")
        validate_non_empty_list(prices, "Список цен пустой")

        return dates, prices
