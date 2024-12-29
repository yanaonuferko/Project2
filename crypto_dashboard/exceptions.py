"""
Модуль для определения пользовательских исключений в проекте.
"""

class CryptoDashboardError(Exception):
    """
    Базовое исключение для всех ошибок в проекте Crypto Dashboard.
    """
    pass


class APIError(CryptoDashboardError):
    """
    Исключение для ошибок, связанных с запросами к API.
    """
    def __init__(self, status_code: int, message: str = "Ошибка API"):
        # Код ошибки API и сообщение, описывающее проблему
        super().__init__(f"{message}: статус {status_code}")
        self.status_code = status_code


class DataValidationError(CryptoDashboardError):
    """
    Исключение для ошибок, связанных с проверкой данных.
    """
    def __init__(self, message: str = "Ошибка проверки данных"):
        # Сообщение, описывающее ошибку валидации данных
        super().__init__(message)


class ChartError(CryptoDashboardError):
    """
    Исключение для ошибок, связанных с построением графиков.
    """
    def __init__(self, message: str = "Ошибка построения графика"):
        # Сообщение об ошибке при создании графика
        super().__init__(message)


class EmptyDataError(CryptoDashboardError):
    """
    Исключение для случаев, когда данные отсутствуют или пусты.
    """
    def __init__(self, message: str = "Данные отсутствуют"):
        # Сообщение об отсутствии данных
        super().__init__(message)
