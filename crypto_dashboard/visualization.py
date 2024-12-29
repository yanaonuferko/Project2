"""
Модуль для визуализации данных с использованием Plotly.
"""

import plotly.graph_objs as go
from typing import List, Union
from datetime import datetime
from .exceptions import ChartError, DataValidationError
from .validation import validate_non_empty_list, validate_matching_lengths, validate_numeric_list


class Visualization:
    """
    Класс для визуализации данных.
    """

    @staticmethod
    def plot_price_trend(dates: List[Union[int, float, str]], prices: List[float], crypto_name: str, period: str):
        """
        Строит график изменения цен криптовалюты.

        :param dates: Список дат в формате timestamp или строки.
        :param prices: Список цен.
        :param crypto_name: Название криптовалюты.
        :param period: Период анализа.
        :raises: DataValidationError, ChartError
        """
        # Валидация входных данных
        validate_non_empty_list(dates, "Список дат пустой")
        validate_non_empty_list(prices, "Список цен пустой")
        validate_matching_lengths(dates, prices, "Длины списков дат и цен не совпадают")
        validate_numeric_list(prices, "Список цен содержит некорректные данные")

        # Проверка на пустое название криптовалюты
        if not crypto_name.strip():
            raise DataValidationError("Название криптовалюты не может быть пустым")

        # Проверка на пустой период
        if not period.strip():
            raise DataValidationError("Период не может быть пустым")

        try:
            # Преобразуем timestamps или строки дат в читаемые даты
            readable_dates = []
            for date in dates:
                if isinstance(date, (int, float)):  # Если это timestamp
                    readable_dates.append(datetime.fromtimestamp(float(date) / 1000).strftime('%Y-%m-%d %H:%M'))
                elif isinstance(date, str):  # Если это строка
                    readable_dates.append(date)
                else:
                    raise DataValidationError("Некорректный формат даты")

            # Создание графика
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=readable_dates, y=prices, mode='lines', name='Цена'))

            # Настройка оформления графика
            fig.update_layout(
                title=f'График цен {crypto_name.capitalize()} за период {period}',
                xaxis_title='Дата и время',
                yaxis_title='Цена (USD)',
                template='plotly',
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )

            # Отображение графика
            fig.show()
        except Exception as e:
            # Обработка ошибок при построении графика
            raise ChartError(f"Ошибка при построении графика: {e}")
