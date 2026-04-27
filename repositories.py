from database import get_connection
from models import Expense, BudgetLimit
from datetime import date
from typing import List, Optional

class ExpenseRepository:
    @staticmethod
    def add(expense: Expense) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
                (expense.amount, expense.category, expense.date.isoformat(), expense.description)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all() -> List[Expense]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, amount, category, date, description FROM expenses")
            rows = cursor.fetchall()
            return [Expense(id=r[0], amount=r[1], category=r[2], date=date.fromisoformat(r[3]), description=r[4]) for r in rows]

    @staticmethod
    def get_by_date_range(start_date: date, end_date: date) -> List[Expense]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, amount, category, date, description FROM expenses WHERE date BETWEEN ? AND ?",
                (start_date.isoformat(), end_date.isoformat())
            )
            rows = cursor.fetchall()
            return [Expense(id=r[0], amount=r[1], category=r[2], date=date.fromisoformat(r[3]), description=r[4]) for r in rows]

class BudgetLimitRepository:
    @staticmethod
    def set_limit(limit: BudgetLimit) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO budget_limits (category, limit_amount, month, year) VALUES (?, ?, ?, ?)",
                (limit.category, limit.limit_amount, limit.month, limit.year)
            )
            conn.commit()

    @staticmethod
    def get_limit(category: str, month: int, year: int) -> Optional[BudgetLimit]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT category, limit_amount, month, year FROM budget_limits WHERE category=? AND month=? AND year=?",
                (category, month, year)
            )
            row = cursor.fetchone()
            if row:
                return BudgetLimit(category=row[0], limit_amount=row[1], month=row[2], year=row[3])
            return None