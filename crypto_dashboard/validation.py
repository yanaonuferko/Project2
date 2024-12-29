"""
Модуль для валидации данных.
"""
from typing import List
from crypto_dashboard.exceptions import DataValidationError

def validate_non_empty_list(data: List, error_message: str = "Список не должен быть пустым") -> None:
    """
    Проверяет, что список не пустой.

    :param data: Список данных для проверки.
    :param error_message: Сообщение об ошибке в случае, если список пустой.
    :raises DataValidationError: Если список пустой.
    """
    if not data:
        raise DataValidationError(error_message)

def validate_matching_lengths(list1: List, list2: List, error_message: str = "Списки должны иметь одинаковую длину") -> None:
    """
    Проверяет, что два списка имеют одинаковую длину.

    :param list1: Первый список.
    :param list2: Второй список.
    :param error_message: Сообщение об ошибке в случае несовпадения длины.
    :raises DataValidationError: Если длины списков не совпадают.
    """
    if len(list1) != len(list2):
        raise DataValidationError(error_message)

def validate_numeric_list(data: List, error_message: str = "Список должен содержать только числовые значения") -> None:
    """
    Проверяет, что список содержит только числовые значения.

    :param data: Список данных для проверки.
    :param error_message: Сообщение об ошибке в случае, если список содержит нечисловые значения.
    :raises DataValidationError: Если список содержит нечисловые значения.
    """
    if not all(isinstance(item, (int, float)) for item in data):
        raise DataValidationError(error_message)
