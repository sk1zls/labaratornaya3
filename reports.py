from datetime import date, timedelta
from typing import Dict, List
from models import Expense
from services import ExpenseService

class ReportFactory:
    @staticmethod
    def create_daily_report(day: date) -> Dict:
        expenses = ExpenseService.get_expenses_by_date_range(day, day)
        return ReportFactory._build_report(expenses, day, day)

    @staticmethod
    def create_weekly_report(end_date: date) -> Dict:
        start = end_date - timedelta(days=6)
        expenses = ExpenseService.get_expenses_by_date_range(start, end_date)
        return ReportFactory._build_report(expenses, start, end_date)

    @staticmethod
    def create_monthly_report(year: int, month: int) -> Dict:
        start = date(year, month, 1)
        if month == 12:
            end = date(year+1, 1, 1) - timedelta(days=1)
        else:
            end = date(year, month+1, 1) - timedelta(days=1)
        expenses = ExpenseService.get_expenses_by_date_range(start, end)
        return ReportFactory._build_report(expenses, start, end)

    @staticmethod
    def _build_report(expenses: List[Expense], start: date, end: date) -> Dict:
        total = sum(e.amount for e in expenses)
        by_category: Dict[str, float] = {}
        for e in expenses:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount
        return {
            "period": f"{start} - {end}",
            "total": total,
            "by_category": by_category,
            "expenses": expenses
        }