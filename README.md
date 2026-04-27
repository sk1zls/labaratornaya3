# Трекер расходов

Консольное приложение для учёта личных финансов с возможностью установки бюджетных лимитов, генерации отчётов и визуализации расходов.

## Функциональность
- Добавление расходов с указанием суммы, категории, даты и описания
- Категоризация расходов (произвольные названия)
- Установка месячных лимитов на категории
- Автоматическое предупреждение при превышении лимита
- Отчёты: ежедневный, еженедельный, ежемесячный
- Визуализация расходов по категориям (круговая диаграмма)

## Технологии
- Python 3.10+
- SQLite3 (встроенная)
- Matplotlib для графиков

## Архитектура
- **Модели** (`models.py`) – dataclasses для Expense, BudgetLimit
- **Репозитории** (`repositories.py`) – абстракция доступа к БД (паттерн Repository)
- **Сервисы** (`services.py`) – бизнес-логика, проверка лимитов
- **Фабрика отчётов** (`reports.py`) – создание отчётов разных типов
- **Визуализация** (`visualization.py`) – построение круговой диаграммы
- **CLI** (`cli.py`) – консольный интерфейс пользователя
- **Точка входа** (`main.py`) – инициализация БД и запуск

```mermaid
classDiagram
    class Expense {
        +int id
        +float amount
        +str category
        +date date
        +str description
    }
    class BudgetLimit {
        +str category
        +float limit_amount
        +int month
        +int year
    }
    class ExpenseRepository {
        +add(Expense) int
        +get_all() List[Expense]
        +get_by_date_range(date, date) List[Expense]
    }
    class BudgetLimitRepository {
        +set_limit(BudgetLimit)
        +get_limit(str, int, int) BudgetLimit
    }
    class ExpenseService {
        +add_expense(...)
        +get_total_for_category_month(...)
        +get_expenses_by_date_range(...)
    }
    class BudgetService {
        +set_budget(...)
    }
    class ReportFactory {
        +create_daily_report(date) dict
        +create_weekly_report(date) dict
        +create_monthly_report(int, int) dict
    }
```

## Скриншоты работы приложения

![Главное меню](screenshots/menu.png)

![Добавление расхода](screenshots/add_expense.png)

![Отчёт за день](screenshots/report.png)

![Круговая диаграмма расходов](screenshots/chart.png)