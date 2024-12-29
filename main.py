import sys
from crypto_dashboard.data_fetcher import DataFetcher
from crypto_dashboard.visualization import Visualization
from crypto_dashboard.exceptions import DataValidationError, APIError


def main():
    print("Добро пожаловать в Crypto Dashboard!")

    crypto = None  # Переменная для хранения выбранной криптовалюты
    period = None  # Переменная для хранения периода анализа

    try:
        while True:
            # Меню выбора действия
            print("\n--- Crypto Dashboard ---")
            print("1. Выбрать криптовалюту")
            print("2. Задать период анализа")
            print("3. Построить график")
            print("4. Выйти")

            choice = input("\nВыберите действие: ")  # Ввод выбора действия

            if choice == "1":
                # Обработка выбора криптовалюты
                try:
                    supported_assets = DataFetcher.fetch_supported_assets()  # Загрузка доступных криптовалют
                    crypto = input("Введите название криптовалюты: ").strip().lower()
                    if crypto not in supported_assets:
                        print("Ошибка: Выбранная криптовалюта недоступна. Попробуйте снова.")
                        crypto = None  # Сбросить выбор
                    else:
                        print(f"Вы выбрали: {crypto.capitalize()}")
                except APIError as e:
                    print(f"Ошибка при загрузке списка доступных криптовалют: {e}")

            elif choice == "2":
                # Обработка выбора периода анализа
                try:
                    period = int(input("Введите количество дней для анализа (например, 7, 14, 30): "))
                    if period <= 0:
                        raise ValueError("Период должен быть положительным числом.")
                    print(f"Выбрано: {period} дней")
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "3":
                # Обработка построения графика
                if not crypto or not period:
                    print("Ошибка: Сначала выберите криптовалюту и задайте период анализа.")
                    continue

                try:
                    print("Получение данных...")
                    dates, prices = DataFetcher.fetch_market_chart(crypto, period)  # Получение данных
                    Visualization.plot_price_trend(dates, prices, crypto_name=crypto, period=f"{period} дней")
                except (APIError, DataValidationError) as e:
                    print(f"Ошибка: {e}")

            elif choice == "4":
                # Завершение работы программы
                print("До свидания!")
                break

            else:
                # Обработка неверного ввода
                print("Ошибка: Неверный выбор. Попробуйте снова.")

    except KeyboardInterrupt:
        # Обработка прерывания программы пользователем
        print("\nВыход из программы. До свидания!")
        sys.exit()

if __name__ == "__main__":
    main()
