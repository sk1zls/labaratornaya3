from datetime import date
from typing import List, Dict
from models import Expense, BudgetLimit
from repositories import ExpenseRepository, BudgetLimitRepository

class ExpenseService:
    @staticmethod
    def add_expense(amount: float, category: str, expense_date: date, description: str = "") -> bool:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        expense = Expense(id=None, amount=amount, category=category, date=expense_date, description=description)
        ExpenseRepository.add(expense)
        # Проверка лимита (только предупреждение, не блокируем)
        limit = BudgetLimitRepository.get_limit(category, expense_date.month, expense_date.year)
        if limit:
            # сумма расходов за текущий месяц по этой категории
            total = ExpenseService.get_total_for_category_month(category, expense_date.year, expense_date.month)
            if total > limit.limit_amount:
                print(f"⚠️ Предупреждение: превышен лимит {limit.limit_amount} по категории '{category}' на месяц!")
        return True

    @staticmethod
    def get_total_for_category_month(category: str, year: int, month: int) -> float:
        start = date(year, month, 1)
        if month == 12:
            end = date(year+1, 1, 1)
        else:
            end = date(year, month+1, 1)
        expenses = ExpenseRepository.get_by_date_range(start, end)
        return sum(e.amount for e in expenses if e.category == category)

    @staticmethod
    def get_expenses_by_date_range(start: date, end: date) -> List[Expense]:
        return ExpenseRepository.get_by_date_range(start, end)

class BudgetService:
    @staticmethod
    def set_budget(category: str, limit_amount: float, month: int, year: int) -> None:
        if limit_amount <= 0:
            raise ValueError("Лимит должен быть положительным")
        limit = BudgetLimit(category=category, limit_amount=limit_amount, month=month, year=year)
        BudgetLimitRepository.set_limit(limit)