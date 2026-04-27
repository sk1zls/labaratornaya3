from datetime import date, datetime
from services import ExpenseService, BudgetService
from reports import ReportFactory
from visualization import show_pie_chart

def main_menu():
    while True:
        print("\n=== Трекер расходов ===")
        print("1. Добавить расход")
        print("2. Установить бюджетный лимит на месяц")
        print("3. Ежедневный отчёт (сегодня)")
        print("4. Еженедельный отчёт")
        print("5. Ежемесячный отчёт")
        print("6. Визуализация расходов за период")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_expense_flow()
        elif choice == "2":
            set_budget_flow()
        elif choice == "3":
            daily_report_flow()
        elif choice == "4":
            weekly_report_flow()
        elif choice == "5":
            monthly_report_flow()
        elif choice == "6":
            visualization_flow()
        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова.")

def add_expense_flow():
    try:
        amount = float(input("Сумма: "))
        category = input("Категория (например: Еда, Транспорт): ").strip()
        date_str = input("Дата (YYYY-MM-DD, оставьте пустым для сегодня): ").strip()
        if date_str:
            expense_date = date.fromisoformat(date_str)
        else:
            expense_date = date.today()
        desc = input("Описание (необязательно): ").strip()
        ExpenseService.add_expense(amount, category, expense_date, desc)
        print("✅ Расход добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def set_budget_flow():
    try:
        category = input("Категория: ").strip()
        limit = float(input("Месячный лимит: "))
        year = int(input("Год (или Enter для текущего): ") or date.today().year)
        month = int(input("Месяц (1-12): "))
        BudgetService.set_budget(category, limit, month, year)
        print("✅ Лимит установлен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def daily_report_flow():
    today = date.today()
    rep = ReportFactory.create_daily_report(today)
    print(f"\n📊 Отчёт за {rep['period']}")
    print(f"Итого: {rep['total']:.2f}")
    if rep['by_category']:
        print("По категориям:")
        for cat, amt in rep['by_category'].items():
            print(f"  {cat}: {amt:.2f}")
    else:
        print("Нет расходов.")

def weekly_report_flow():
    end = date.today()
    rep = ReportFactory.create_weekly_report(end)
    print(f"\n📊 Отчёт за {rep['period']}")
    print(f"Итого: {rep['total']:.2f}")
    if rep['by_category']:
        print("По категориям:")
        for cat, amt in rep['by_category'].items():
            print(f"  {cat}: {amt:.2f}")
    else:
        print("Нет расходов.")

def monthly_report_flow():
    year = int(input("Год: "))
    month = int(input("Месяц (1-12): "))
    rep = ReportFactory.create_monthly_report(year, month)
    print(f"\n📊 Отчёт за {rep['period']}")
    print(f"Итого: {rep['total']:.2f}")
    if rep['by_category']:
        print("По категориям:")
        for cat, amt in rep['by_category'].items():
            print(f"  {cat}: {amt:.2f}")
    else:
        print("Нет расходов.")

def visualization_flow():
    print("Визуализация за период:")
    start = input("Начальная дата (YYYY-MM-DD): ").strip()
    end = input("Конечная дата (YYYY-MM-DD): ").strip()
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        expenses = ExpenseService.get_expenses_by_date_range(start_date, end_date)
        by_category = {}
        for e in expenses:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount
        show_pie_chart(by_category, f"Расходы с {start_date} по {end_date}")
    except Exception as e:
        print(f"Ошибка в датах: {e}")